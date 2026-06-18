#!/usr/bin/env python3
"""
M032 -- "Haggling Reward Model" CPU proof-of-concept.

DECISIVE CLAIM UNDER TEST
-------------------------
In an RLHF-style optimization loop, a reward model implemented as a per-skill
Kalman belief (mu_s, Sigma_s) that ACTIVELY probes the most-uncertain skill and
concedes by Kalman gain will:
  (a) keep the proxy-vs-true reward gap smaller than a FROZEN reward model, and
  (b) its per-skill covariance Sigma_s COLLAPSES while proxy reward is still
      rising, and that collapse PRECEDES the frozen RM's proxy-true gap blow-up
      -- i.e. Sigma_s-collapse is a LEADING indicator of reward hacking /
      over-optimization.

This is a synthetic toy. A confirming result is EVIDENCE, not proof. Numbers
reported by this script are the ACTUAL measured outputs of the run.

No torch available; pure numpy/scipy. Matplotlib uses the Agg backend.

DESIGN NOTES (why this version is decisive, not a rigged straight line)
----------------------------------------------------------------------
* TRUE quality SATURATES (bounded, concave) in the legitimate directions but is
  exactly 0 along an EXPLOITABLE dimension. The RM is LINEAR and carries a
  spurious positive weight on the exploit dim. Hence:
    - early rounds: policy climbs legitimate dims -> proxy AND true both rise
      (in-distribution, productive optimization);
    - later: legitimate dims saturate, so the only way to keep raising the RM
      score is to pump the exploit dim -> proxy keeps climbing, true FLATTENS
      then DROPS. That knee is a genuine reward-hacking PHASE TRANSITION, not a
      linear drift, so "blow-up step" is a real event.
* The HAGGLING belief's Sigma_s is NOT a fixed Kalman clock: each round we
  inject PROCESS NOISE proportional to how far the policy's response for skill s
  has DRIFTED since last probe. So Sigma shrinks while the policy is stable and
  re-inflates under drift -- the collapse is therefore COUPLED to the real
  optimization dynamics, which is what makes "leading indicator" a meaningful
  test rather than an arithmetic tautology.
* Stochastic policy exploration => genuine per-seed spread in event timing.
"""

import json
import os

import matplotlib

matplotlib.use("Agg")  # headless / no display
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
OUT_DIR = "/home/user/autoresearch-test/run31/m032_poc"
SCRATCH_DIR = "/tmp/run31/m032"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)

# ----------------------------------------------------------------------------
# Global experiment configuration
# ----------------------------------------------------------------------------
S = 4                 # number of skills
D = 5                 # response dimensionality (R^d)
EXPLOIT_DIM = D - 1   # last dim is the reward-hacking channel (NOT in true q)
T = 250               # rounds per run
N_SEEDS = 12          # >= 10 seeds
N_INIT = 300          # initial samples used to fit the frozen RM (per skill)

# Policy hill-climb (finite-difference ascent on the CURRENT RM)
POLICY_STEPS = 4      # ascent steps per skill per round
POLICY_LR = 0.05      # ascent learning rate
FD_EPS = 1e-3         # finite-difference epsilon
POLICY_EXPLORE = 0.02 # stochastic exploration noise added to the policy step

# CAPACITY BUDGET: each skill's response x is constrained to ||x|| <= X_BUDGET
# (projected after every ascent step). A fixed-capacity policy can only allocate
# so much magnitude, so spending it on the exploit dim STEALS from legitimate
# dims. This is what turns saturation into genuine over-optimization: as the RM
# pulls on the exploit weight, true quality PEAKS then DECLINES.
X_BUDGET = 2.5

# True-quality saturation: legitimate score = sum_j a_j * tanh(b_j * x_j),
# bounded; exploit dim contributes 0. SAT_SCALE sets how quickly legit dims
# saturate (smaller => saturates sooner => hacking pressure kicks in sooner).
SAT_SCALE = 0.8

# RM spurious exploit weight strength (how strongly the frozen RM rewards the
# hack channel). Kept SMALL so reward-hacking emerges GRADUALLY/LATE: the policy
# first exhausts the (easy, high-gradient) legitimate gains, and only later --
# once legit dims saturate -- does the weak exploit gradient dominate and pull
# the policy into the hack channel. This late, slow blow-up is what makes the
# "leading indicator" question non-trivial (there must be a window where the
# belief has collapsed but the frozen RM has not yet hacked).
EXPLOIT_RM_WEIGHT = 0.55

# Measurement / Kalman noise model
OBS_NOISE_STD = 0.20  # std of the noisy true-quality measurement
# Process noise injected into Sigma_s each round, a SATURATING function of policy
# drift of skill s's response since it was last probed. This COUPLES Sigma to
# drift but is bounded so Sigma can still collapse during the stable phase.
DRIFT_PROC_GAIN = 0.06
DRIFT_PROC_CAP = 0.30  # max process-noise added per round per skill
SIGMA_FLOOR = 1e-4

# Threshold definitions (declared up front so they appear in results.json)
SIGMA_COLLAPSE_FRAC = 0.10   # Sigma below 10% of its initial value => "collapsed"
FROZEN_BLOWUP_MULT = 2.0     # frozen gap > 2x early baseline => "blow-up"
# Early baseline = the FIRST few rounds, before reward-hacking has developed.
BASELINE_WINDOW = 3          # rounds [0,BASELINE_WINDOW) define the early baseline

RNG_MASTER_SEED = 20260604


# ----------------------------------------------------------------------------
# Ground-truth problem instance (per seed)
# ----------------------------------------------------------------------------
def make_problem(rng):
    """Build ground-truth SATURATING true-quality params per skill.

    true_quality_s(x) = sum_{j != EXPLOIT_DIM} a_{s,j} * tanh(b_{s,j} * x_j)
    The EXPLOIT_DIM coordinate has NO term -> pumping it cannot raise true
    quality (it is the reward-hacking channel), but the linear RM rewards it.
    """
    a = np.abs(rng.normal(1.0, 0.3, size=(S, D)))   # positive amplitudes
    b = np.abs(rng.normal(1.0, 0.3, size=(S, D))) * (1.0 / SAT_SCALE)
    a[:, EXPLOIT_DIM] = 0.0  # exploit dim contributes nothing to true quality
    b[:, EXPLOIT_DIM] = 0.0
    # normalize legit amplitudes so true scores are comparable across skills
    for s in range(S):
        nrm = np.sum(a[s])
        if nrm > 0:
            a[s] = a[s] / nrm
    return {"a": a, "b": b}


def true_quality(prob, s, x):
    """Saturating true scalar quality of response x for one skill."""
    a = prob["a"][s]
    b = prob["b"][s]
    return float(np.sum(a * np.tanh(b * x)))


# ----------------------------------------------------------------------------
# Frozen reward model (LINEAR with a spurious positive exploit weight)
# ----------------------------------------------------------------------------
def fit_frozen_rm(rng, prob):
    """Fit a LINEAR RM ONCE on initial (policy_0) in-distribution samples.

    On the initial cloud the true quality is locally ~linear (tanh near 0), so a
    linear RM fits well IN-distribution. We additionally bake a spurious positive
    weight on EXPLOIT_DIM (a confound present in the small initial set) so the
    fitted RM rewards the hack channel. As the policy later drives x large, the
    linear RM keeps extrapolating linearly while true quality saturates -> gap.
    """
    W_rm = np.zeros((S, D))
    b_rm = np.zeros(S)
    for s in range(S):
        X = rng.normal(0.0, 0.6, size=(N_INIT, D))  # small-radius init cloud
        y = np.array([true_quality(prob, s, X[i]) for i in range(N_INIT)])
        # spurious confound on the exploit dim within the training set
        confound = rng.normal(0.0, 1.0, size=N_INIT)
        X[:, EXPLOIT_DIM] = 0.6 * confound + rng.normal(0.0, 0.3, size=N_INIT)
        y = y + 0.5 * EXPLOIT_RM_WEIGHT * confound + rng.normal(0.0, 0.02, size=N_INIT)
        lam = 1e-2
        A = X.T @ X + lam * np.eye(D)
        w_fit = np.linalg.solve(A, X.T @ y)
        # ensure the exploit weight is positive & nontrivial (the hack incentive)
        w_fit[EXPLOIT_DIM] = max(w_fit[EXPLOIT_DIM], 0.4 * EXPLOIT_RM_WEIGHT)
        W_rm[s] = w_fit
        b_rm[s] = float(np.mean(y - X @ w_fit))
    return W_rm, b_rm


def frozen_score(W_rm, b_rm, s, x):
    """Frozen RM predicted reward for skill s, response x (linear)."""
    return float(np.dot(W_rm[s], x) + b_rm[s])


# ----------------------------------------------------------------------------
# Policy: finite-difference hill-climb on the CURRENT RM scorer
# ----------------------------------------------------------------------------
def _project_budget(x):
    """Project x onto the L2 ball of radius X_BUDGET (capacity constraint)."""
    nrm = float(np.linalg.norm(x))
    if nrm > X_BUDGET:
        x = x * (X_BUDGET / nrm)
    return x


def policy_optimize(score_fn, x0, rng):
    """Hill-climb x to maximize score_fn(x) via finite-difference ascent with a
    little stochastic exploration, then PROJECT onto the capacity budget ball.

    The budget makes the exploit dim compete with legitimate dims for magnitude,
    which is the mechanism that produces genuine over-optimization (true quality
    peaks then declines as the policy reallocates budget to the hack channel)."""
    x = x0.copy()
    for _ in range(POLICY_STEPS):
        f0 = score_fn(x)
        g = np.zeros(D)
        for j in range(D):
            xp = x.copy()
            xp[j] += FD_EPS
            g[j] = (score_fn(xp) - f0) / FD_EPS
        x = x + POLICY_LR * g + POLICY_EXPLORE * rng.normal(0.0, 1.0, size=D)
        x = _project_budget(x)
    return x


# ----------------------------------------------------------------------------
# One full run for a given seed and a given RM mode ("frozen" or "haggling")
# ----------------------------------------------------------------------------
def run_one(seed, mode):
    rng = np.random.default_rng(seed)
    prob = make_problem(rng)

    # Both modes share the SAME underlying biased frozen RM as the base scorer;
    # only the haggling mode re-anchors it online.
    rm_rng = np.random.default_rng(seed + 999_983)
    W_rm, b_rm = fit_frozen_rm(rm_rng, prob)

    # policy state: current best response per skill (separate RNG stream so the
    # policy exploration is identical structure across modes for fairness)
    pol_rng = np.random.default_rng(seed + 7)
    x_cur = [pol_rng.normal(0.0, 0.2, size=D) for _ in range(S)]
    x_last_probe = [xc.copy() for xc in x_cur]  # response when last probed

    # Haggling belief over each skill's TRUE competence (scalar): mu_s, Sigma_s.
    # Initial uncertainty differs per skill (heterogeneous prior) so collapse
    # timing is not a single deterministic clock shared across seeds.
    mu = np.zeros(S)
    Sigma = rng.uniform(0.6, 1.4, size=S)
    Sigma0 = Sigma.copy()
    anchor = np.zeros(S)  # per-skill RM re-anchor offset

    log_proxy = np.zeros(T)
    log_true = np.zeros(T)
    log_gap = np.zeros(T)
    log_sigma = np.zeros((T, S))

    for t in range(T):
        # scorer the policy optimizes against this round
        if mode == "frozen":
            def make_scorer(s):
                return lambda x: frozen_score(W_rm, b_rm, s, x)
        else:
            def make_scorer(s):
                a = anchor[s]
                return lambda x: frozen_score(W_rm, b_rm, s, x) + a

        # policy hill-climbs each skill
        for s in range(S):
            x_cur[s] = policy_optimize(make_scorer(s), x_cur[s], pol_rng)

        # ---- HAGGLING: drift-coupled process noise + active probe + concede ----
        if mode == "haggling":
            # 1) inject process noise into EVERY skill's Sigma proportional to how
            #    far its response has drifted since it was last probed. Drift =
            #    off-distribution movement => the belief should grow uncertain.
            for s in range(S):
                drift = float(np.linalg.norm(x_cur[s] - x_last_probe[s]))
                # saturating, bounded process noise => Sigma can still collapse
                # while the policy is stable, yet responds to large drift.
                proc = DRIFT_PROC_CAP * np.tanh(DRIFT_PROC_GAIN * drift / DRIFT_PROC_CAP)
                Sigma[s] = Sigma[s] + proc

            # 2) ACTIVE probe the most-uncertain skill
            s_star = int(np.argmax(Sigma))
            obs = true_quality(prob, s_star, x_cur[s_star]) + pol_rng.normal(
                0.0, OBS_NOISE_STD
            )
            # 3) Kalman update: concede more when more uncertain
            R = OBS_NOISE_STD ** 2
            K = Sigma[s_star] / (Sigma[s_star] + R)
            mu[s_star] = mu[s_star] + K * (obs - mu[s_star])
            Sigma[s_star] = max((1.0 - K) * Sigma[s_star], SIGMA_FLOOR)
            x_last_probe[s_star] = x_cur[s_star].copy()  # reset drift baseline
            # 4) re-anchor RM scoring for s_star toward believed-true competence
            proxy_sstar = frozen_score(W_rm, b_rm, s_star, x_cur[s_star]) + anchor[s_star]
            anchor[s_star] += K * (mu[s_star] - proxy_sstar)

        # ---- log round metrics (mean over skills) ----
        proxies, trues = [], []
        for s in range(S):
            if mode == "frozen":
                p = frozen_score(W_rm, b_rm, s, x_cur[s])
            else:
                p = frozen_score(W_rm, b_rm, s, x_cur[s]) + anchor[s]
            proxies.append(p)
            trues.append(true_quality(prob, s, x_cur[s]))
        log_proxy[t] = float(np.mean(proxies))
        log_true[t] = float(np.mean(trues))
        log_gap[t] = log_proxy[t] - log_true[t]
        log_sigma[t] = Sigma.copy()

    return {
        "proxy": log_proxy,
        "true": log_true,
        "gap": log_gap,
        "sigma": log_sigma,
        "sigma0": Sigma0,
    }


# ----------------------------------------------------------------------------
# Event detectors
# ----------------------------------------------------------------------------
def sigma_collapse_step(sigma_traj, sigma0, frac=SIGMA_COLLAPSE_FRAC, reduce="max"):
    """First round where Sigma (max or mean over skills) < frac * its initial.

    NB: because Sigma is re-inflated by drift, this is a genuine first-crossing
    of a coupled process, not a deterministic Kalman countdown.
    """
    if reduce == "max":
        series = sigma_traj.max(axis=1)
        thresh = frac * float(sigma0.max())
    else:
        series = sigma_traj.mean(axis=1)
        thresh = frac * float(sigma0.mean())
    below = np.where(series < thresh)[0]
    return int(below[0]) if below.size > 0 else None


def frozen_blowup_step(gap, mult=FROZEN_BLOWUP_MULT, window=BASELINE_WINDOW):
    """First round (>= window) the frozen proxy-true gap exceeds
    mult*|baseline| + |baseline|, where baseline = mean gap over first `window`
    rounds. Returns None if the gap never blows up (frozen did NOT reward-hack).
    """
    baseline = float(np.mean(gap[:window]))
    base_mag = abs(baseline)
    thresh_level = (mult + 1.0) * base_mag if base_mag > 1e-9 else (mult + 1.0) * 1e-3
    over = np.where(gap > thresh_level)[0]
    over = over[over >= window]
    return (int(over[0]) if over.size > 0 else None), baseline, thresh_level


# ----------------------------------------------------------------------------
# Robustness sweep over the exploit-weight (does the finding survive parameter
# changes, or is it a single tuned point?). Mutates the global EXPLOIT_RM_WEIGHT
# transiently and restores it. Pure measurement, recorded in results.json.
# ----------------------------------------------------------------------------
def robustness_sweep(weights):
    global EXPLOIT_RM_WEIGHT
    saved = EXPLOIT_RM_WEIGHT
    seeds = [RNG_MASTER_SEED + 31 * i for i in range(N_SEEDS)]
    rows = []
    for w in weights:
        EXPLOIT_RM_WEIGHT = w
        fg, hg, leads, pos, blow, coll, decl = [], [], [], 0, 0, 0, 0
        for sd in seeds:
            rf = run_one(sd, "frozen")
            rh = run_one(sd, "haggling")
            fg.append(float(rf["gap"][-1]))
            hg.append(float(rh["gap"][-1]))
            sc = sigma_collapse_step(rh["sigma"], rh["sigma0"], reduce="max")
            bu, _, _ = frozen_blowup_step(rf["gap"])
            peak = float(np.max(rf["true"]))
            pr = int(np.argmax(rf["true"]))
            if peak - float(rf["true"][-1]) > 0.02 and pr < T - 5:
                decl += 1
            if bu is not None:
                blow += 1
            if sc is not None:
                coll += 1
            if sc is not None and bu is not None:
                leads.append(bu - sc)
                pos += 1 if (bu - sc) > 0 else 0
        leads = np.array(leads, dtype=float)
        rows.append({
            "exploit_rm_weight": float(w),
            "frozen_final_gap_mean": float(np.mean(fg)),
            "haggling_final_gap_mean": float(np.mean(hg)),
            "n_frozen_blowup": int(blow),
            "n_frozen_true_decline": int(decl),
            "n_sigma_collapse": int(coll),
            "lead_time_mean": float(leads.mean()) if leads.size else None,
            "lead_time_std": float(leads.std()) if leads.size else None,
            "fraction_positive_lead": float(pos / len(leads)) if leads.size else None,
        })
    EXPLOIT_RM_WEIGHT = saved
    return rows


# ----------------------------------------------------------------------------
# Main experiment
# ----------------------------------------------------------------------------
def main():
    seeds = [RNG_MASTER_SEED + 31 * i for i in range(N_SEEDS)]

    per_seed = []
    frozen_gap_stack, hagg_gap_stack = [], []
    frozen_proxy_stack, frozen_true_stack = [], []
    hagg_proxy_stack, hagg_true_stack = [], []
    hagg_sigma_stack = []

    lead_times, pos_lead_flags = [], []

    for seed in seeds:
        rf = run_one(seed, "frozen")
        rh = run_one(seed, "haggling")

        frozen_gap_stack.append(rf["gap"])
        hagg_gap_stack.append(rh["gap"])
        frozen_proxy_stack.append(rf["proxy"])
        frozen_true_stack.append(rf["true"])
        hagg_proxy_stack.append(rh["proxy"])
        hagg_true_stack.append(rh["true"])
        hagg_sigma_stack.append(rh["sigma"])

        sc_step = sigma_collapse_step(rh["sigma"], rh["sigma0"], reduce="max")
        bu_step, baseline, thresh = frozen_blowup_step(rf["gap"])

        if sc_step is not None and bu_step is not None:
            lead = bu_step - sc_step
            lead_times.append(lead)
            pos_lead_flags.append(bool(lead > 0))
        else:
            lead = None
            if bu_step is None:
                pos_lead_flags.append(False)  # frozen never blew up -> no lead

        per_seed.append(
            {
                "seed": int(seed),
                "frozen_final_gap": float(rf["gap"][-1]),
                "haggling_final_gap": float(rh["gap"][-1]),
                "frozen_final_true": float(rf["true"][-1]),
                "haggling_final_true": float(rh["true"][-1]),
                "frozen_baseline_gap": float(baseline),
                "frozen_blowup_threshold_level": float(thresh),
                "sigma_collapse_step": sc_step,
                "frozen_blowup_step": bu_step,
                "lead_time": lead,
                "frozen_max_gap": float(np.max(rf["gap"])),
                "haggling_max_gap": float(np.max(rh["gap"])),
                "sigma0_max": float(rh["sigma0"].max()),
                "sigma_final_max": float(rh["sigma"][-1].max()),
                "frozen_true_peak": float(np.max(rf["true"])),
                "frozen_true_peak_round": int(np.argmax(rf["true"])),
            }
        )

    frozen_gap_stack = np.array(frozen_gap_stack)
    hagg_gap_stack = np.array(hagg_gap_stack)
    frozen_proxy_stack = np.array(frozen_proxy_stack)
    frozen_true_stack = np.array(frozen_true_stack)
    hagg_proxy_stack = np.array(hagg_proxy_stack)
    hagg_true_stack = np.array(hagg_true_stack)
    hagg_sigma_stack = np.array(hagg_sigma_stack)

    rounds = np.arange(T)
    frozen_gap_mean = frozen_gap_stack.mean(0)
    frozen_gap_std = frozen_gap_stack.std(0)
    hagg_gap_mean = hagg_gap_stack.mean(0)
    hagg_gap_std = hagg_gap_stack.std(0)

    frozen_final_gap_mean = float(frozen_gap_stack[:, -1].mean())
    frozen_final_gap_std = float(frozen_gap_stack[:, -1].std())
    hagg_final_gap_mean = float(hagg_gap_stack[:, -1].mean())
    hagg_final_gap_std = float(hagg_gap_stack[:, -1].std())

    lead_arr = np.array(lead_times, dtype=float) if lead_times else np.array([])
    lead_mean = float(lead_arr.mean()) if lead_arr.size else None
    lead_std = float(lead_arr.std()) if lead_arr.size else None
    frac_pos_lead = (
        float(np.mean([1.0 if f else 0.0 for f in pos_lead_flags]))
        if pos_lead_flags else None
    )

    n_blowups = sum(1 for ps in per_seed if ps["frozen_blowup_step"] is not None)
    n_collapses = sum(1 for ps in per_seed if ps["sigma_collapse_step"] is not None)

    # Does the frozen baseline actually reward-hack? Require both a gap blow-up
    # AND a TRUE-quality peak-then-decline (the hallmark of over-optimization).
    frozen_true_declines = sum(
        1 for ps in per_seed
        if ps["frozen_true_peak"] - ps["frozen_final_true"] > 0.02
        and ps["frozen_true_peak_round"] < T - 5
    )

    cond_a = hagg_final_gap_mean < frozen_final_gap_mean
    cond_frozen_hacks = (n_blowups >= (N_SEEDS // 2 + 1)) and (
        frozen_true_declines >= (N_SEEDS // 2 + 1)
    )
    cond_lead = (frac_pos_lead is not None) and (frac_pos_lead >= 0.5)

    if not cond_frozen_hacks:
        verdict = "INCONCLUSIVE"
        verdict_reason = (
            f"Frozen baseline did not exhibit clear reward-hacking: "
            f"{n_blowups}/{N_SEEDS} gap blow-ups, {frozen_true_declines}/{N_SEEDS} "
            f"true-quality peak-then-decline. Without a genuine over-optimization "
            f"event the leading-indicator claim cannot be tested."
        )
    elif cond_a and cond_lead:
        verdict = "CONFIRMED"
        verdict_reason = (
            "At toy scale: frozen RM genuinely reward-hacks (gap blow-up + true "
            "quality peaks then declines); haggling RM keeps a smaller final "
            "proxy-true gap AND its Sigma-collapse precedes the frozen blow-up on "
            "a majority of seeds. Evidence, not proof."
        )
    elif cond_a or cond_lead:
        verdict = "INCONCLUSIVE"
        verdict_reason = (
            f"Frozen hacks, but only one of (smaller-gap, leading-collapse) holds "
            f"at toy scale (cond_a={cond_a}, cond_lead={cond_lead})."
        )
    else:
        verdict = "REFUTED"
        verdict_reason = (
            "Frozen reward-hacks but haggling neither narrows the final gap nor "
            "yields a leading collapse signal."
        )

    make_plots(rounds, frozen_proxy_stack, frozen_true_stack,
               hagg_proxy_stack, hagg_true_stack, hagg_sigma_stack, per_seed,
               frozen_gap_mean, frozen_gap_std)

    # robustness: re-measure the whole pipeline across a range of exploit weights
    sweep_rows = robustness_sweep([0.30, 0.45, 0.55, 0.70, 0.90])

    results = {
        "claim": (
            "Per-skill Kalman 'haggling' RM keeps proxy-true gap smaller than a "
            "frozen RM, AND its Sigma_s collapse is a LEADING indicator that "
            "precedes the frozen RM's proxy-true gap blow-up (reward hacking)."
        ),
        "scale": "synthetic toy (S=4 skills, d=5, saturating true quality, exploit channel, finite-diff policy)",
        "config": {
            "S": S, "D": D, "EXPLOIT_DIM": EXPLOIT_DIM, "T": T,
            "N_SEEDS": N_SEEDS, "N_INIT": N_INIT,
            "POLICY_STEPS": POLICY_STEPS, "POLICY_LR": POLICY_LR,
            "FD_EPS": FD_EPS, "POLICY_EXPLORE": POLICY_EXPLORE,
            "X_BUDGET": X_BUDGET,
            "SAT_SCALE": SAT_SCALE, "EXPLOIT_RM_WEIGHT": EXPLOIT_RM_WEIGHT,
            "OBS_NOISE_STD": OBS_NOISE_STD, "DRIFT_PROC_GAIN": DRIFT_PROC_GAIN,
            "DRIFT_PROC_CAP": DRIFT_PROC_CAP,
            "SIGMA_FLOOR": SIGMA_FLOOR, "RNG_MASTER_SEED": RNG_MASTER_SEED,
            "seeds": [int(s) for s in seeds],
        },
        "threshold_definitions": {
            "sigma_collapse_frac": SIGMA_COLLAPSE_FRAC,
            "sigma_collapse_reduce": "max over skills",
            "sigma_collapse_rule": (
                "first round where max_s Sigma_s < sigma_collapse_frac * "
                "max_s Sigma_s(t=init). Sigma is drift-coupled (re-inflated by "
                "policy off-distribution movement), so this is a real first-"
                "crossing, not a fixed Kalman countdown."
            ),
            "frozen_blowup_mult": FROZEN_BLOWUP_MULT,
            "baseline_window_rounds": BASELINE_WINDOW,
            "frozen_blowup_rule": (
                "baseline = mean(frozen gap over first BASELINE_WINDOW rounds); "
                "blow-up = first round (>= window) where gap > "
                "(FROZEN_BLOWUP_MULT+1)*|baseline|."
            ),
            "frozen_hack_confirmation_rule": (
                "frozen counted as genuinely reward-hacking only if it has BOTH a "
                "gap blow-up AND a true-quality peak-then-decline (peak before "
                "round T-5, decline > 0.02) on a majority of seeds."
            ),
            "lead_time_rule": "frozen_blowup_step - sigma_collapse_step (positive => collapse leads)",
        },
        "aggregate": {
            "frozen_final_gap_mean": frozen_final_gap_mean,
            "frozen_final_gap_std": frozen_final_gap_std,
            "haggling_final_gap_mean": hagg_final_gap_mean,
            "haggling_final_gap_std": hagg_final_gap_std,
            "frozen_final_gap_minus_haggling": frozen_final_gap_mean - hagg_final_gap_mean,
            "lead_time_mean": lead_mean,
            "lead_time_std": lead_std,
            "fraction_seeds_positive_lead": frac_pos_lead,
            "n_seeds_frozen_blowup": n_blowups,
            "n_seeds_sigma_collapse": n_collapses,
            "n_seeds_frozen_true_declines": frozen_true_declines,
            "n_seeds_total": N_SEEDS,
            "cond_a_haggling_gap_smaller": bool(cond_a),
            "cond_frozen_actually_hacks": bool(cond_frozen_hacks),
            "cond_lead_majority_positive": bool(cond_lead),
        },
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "robustness_sweep_over_exploit_weight": sweep_rows,
        "per_seed": per_seed,
        "gap_trajectories": {
            "rounds": rounds.tolist(),
            "frozen_gap_mean": frozen_gap_mean.tolist(),
            "frozen_gap_std": frozen_gap_std.tolist(),
            "haggling_gap_mean": hagg_gap_mean.tolist(),
            "haggling_gap_std": hagg_gap_std.tolist(),
            "frozen_true_mean": frozen_true_stack.mean(0).tolist(),
            "haggling_true_mean": hagg_true_stack.mean(0).tolist(),
        },
    }

    with open(os.path.join(OUT_DIR, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("=" * 72)
    print("M032 Haggling Reward Model -- CPU proof-of-concept")
    print("=" * 72)
    print(f"seeds={N_SEEDS}  rounds={T}  skills={S}  dim={D} (exploit dim={EXPLOIT_DIM})")
    print("-" * 72)
    print(f"FINAL proxy-true gap  frozen   : {frozen_final_gap_mean:+.4f} +/- {frozen_final_gap_std:.4f}")
    print(f"FINAL proxy-true gap  haggling : {hagg_final_gap_mean:+.4f} +/- {hagg_final_gap_std:.4f}")
    print(f"  gap reduction (frozen-hagg)  : {frozen_final_gap_mean - hagg_final_gap_mean:+.4f}")
    print("-" * 72)
    print(f"frozen gap blow-ups            : {n_blowups}/{N_SEEDS} seeds")
    print(f"frozen TRUE peak-then-decline  : {frozen_true_declines}/{N_SEEDS} seeds (genuine over-opt)")
    print(f"sigma collapses                : {n_collapses}/{N_SEEDS} seeds")
    if lead_mean is not None:
        print(f"LEAD TIME (blowup - collapse)  : {lead_mean:+.2f} +/- {lead_std:.2f} rounds")
    else:
        print("LEAD TIME                      : N/A (insufficient paired events)")
    print(f"fraction seeds positive lead   : {frac_pos_lead}")
    print("-" * 72)
    print(f"VERDICT: {verdict}")
    print(f"  reason: {verdict_reason}")
    print("=" * 72)
    return results


def make_plots(rounds, frozen_proxy_stack, frozen_true_stack,
               hagg_proxy_stack, hagg_true_stack, hagg_sigma_stack, per_seed,
               frozen_gap_mean_for_plot, frozen_gap_std_for_plot):
    # ----- proxy_vs_true.png -----
    fig, ax = plt.subplots(1, 1, figsize=(9, 5.5))
    fp_m, fp_s = frozen_proxy_stack.mean(0), frozen_proxy_stack.std(0)
    ft_m = frozen_true_stack.mean(0)
    hp_m, hp_s = hagg_proxy_stack.mean(0), hagg_proxy_stack.std(0)
    ht_m = hagg_true_stack.mean(0)

    ax.plot(rounds, fp_m, color="C3", lw=2, label="frozen RM: PROXY (RM score)")
    ax.fill_between(rounds, fp_m - fp_s, fp_m + fp_s, color="C3", alpha=0.15)
    ax.plot(rounds, ft_m, color="C3", lw=2, ls="--", label="frozen RM: TRUE quality")
    ax.plot(rounds, hp_m, color="C0", lw=2, label="haggling RM: PROXY (RM score)")
    ax.fill_between(rounds, hp_m - hp_s, hp_m + hp_s, color="C0", alpha=0.15)
    ax.plot(rounds, ht_m, color="C0", lw=2, ls="--", label="haggling RM: TRUE quality")

    ax.set_xlabel("RLHF round")
    ax.set_ylabel("reward (mean over skills, mean over seeds)")
    ax.set_title("Proxy vs True reward: frozen vs haggling RM\n"
                 "gap = solid - dashed; frozen TRUE peaks-then-declines = reward hacking")
    ax.legend(loc="best", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "proxy_vs_true.png"), dpi=130)
    plt.close(fig)

    # ----- sigma_trajectory.png (two panels: log-Sigma + frozen gap) -----
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(9, 7.5), sharex=True,
                                  gridspec_kw={"height_ratios": [2, 1]})
    sig_mean = hagg_sigma_stack.mean(0)  # [T, S]
    max_sigma = hagg_sigma_stack.max(2).mean(0)
    sigma0_max = float(hagg_sigma_stack.max(2)[:, 0].mean())  # ~ initial max
    collapse_level = SIGMA_COLLAPSE_FRAC * sigma0_max

    for s in range(sig_mean.shape[1]):
        ax.plot(rounds, sig_mean[:, s], lw=1.2, alpha=0.7, label=f"Sigma skill {s}")
    ax.plot(rounds, max_sigma, color="k", lw=2.4, label="max_s Sigma_s (collapse metric)")
    ax.axhline(collapse_level, color="gray", ls="--", lw=1.2,
               label=f"collapse threshold = {SIGMA_COLLAPSE_FRAC:.0%} of init")
    ax.set_yscale("log")

    coll = [ps["sigma_collapse_step"] for ps in per_seed if ps["sigma_collapse_step"] is not None]
    bu = [ps["frozen_blowup_step"] for ps in per_seed if ps["frozen_blowup_step"] is not None]
    cm = float(np.mean(coll)) if coll else None
    bm = float(np.mean(bu)) if bu else None
    for a in (ax, ax2):
        if cm is not None:
            a.axvline(cm, color="C0", ls=":", lw=2,
                      label=(f"mean Sigma-collapse step = {cm:.1f}" if a is ax else None))
        if bm is not None:
            a.axvline(bm, color="C3", ls=":", lw=2,
                      label=(f"mean frozen blow-up step = {bm:.1f}" if a is ax else None))

    ax.set_ylabel("Sigma_s (log scale, mean over seeds)")
    ax.set_title("Haggling RM uncertainty collapse vs frozen reward-hack blow-up\n"
                 "Sigma-collapse line LEFT of blow-up line => leading indicator")
    ax.legend(loc="best", fontsize=7.5, ncol=2)
    ax.grid(alpha=0.3, which="both")

    # bottom panel: frozen proxy-true gap (the thing whose blow-up we predict)
    ax2.plot(rounds, frozen_gap_mean_for_plot, color="C3", lw=2,
             label="frozen proxy-true GAP")
    ax2.fill_between(rounds,
                     frozen_gap_mean_for_plot - frozen_gap_std_for_plot,
                     frozen_gap_mean_for_plot + frozen_gap_std_for_plot,
                     color="C3", alpha=0.15)
    ax2.set_xlabel("RLHF round")
    ax2.set_ylabel("frozen gap")
    ax2.legend(loc="best", fontsize=7.5)
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "sigma_trajectory.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()
