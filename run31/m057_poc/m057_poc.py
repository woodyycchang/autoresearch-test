#!/usr/bin/env python3
"""
M057 -- Persistent-Homology Bruise Forensics (CPU proof-of-concept)
===================================================================

DECISIVE CLAIM UNDER TEST
-------------------------
Using the CHECKPOINT TIMELINE as a filtration axis, a feature introduced LATE
in training is DATABLE from the topology of its activation cloud (recover the
injection step K within +/-2 checkpoints), AND a BACKDOOR (trigger->target)
shows a "load-bearing-yet-young" signature -- high final persistence
(entrenched) but late birth and FASTER / more abrupt staging -- versus a
benignly-introduced late capability that emerges more gradually.

DESIGN (toy, CPU only)
----------------------
* Data : sklearn load_digits (8x8, 10 classes), pixels scaled to [0,1].
* Model: MLPClassifier(hidden_layer_sizes=(64,32), warm_start) stepped via
         partial_fit to yield N_CKPT checkpoints. Hidden activations are read
         from the SECOND hidden layer (32-d) by an explicit forward pass.
* Two runs share the schedule with a KNOWN late injection step K:
    RUN A (backdoor): from step K onward, a fraction of each training batch is
        replaced by TRIGGER-stamped inputs (2x2 top-left corner forced to max)
        relabelled to a fixed TARGET class. Model learns trigger->target late.
    RUN B (benign): the held-out class C_NEW is withheld from the LEARNING
        SIGNAL before step K (its examples are still present in batches but
        carry sample_weight = 0, so they contribute no gradient), then is
        legitimately INTRODUCED from step K onward (full weight). Genuinely
        late-learned capability, not malicious. (sklearn's MLPClassifier
        forbids changing the class set across warm-start batches, so class
        exclusion is implemented via gradient masking rather than by dropping
        the rows.)
* Per checkpoint t, build the CONCEPT activation cloud:
    A: hidden activations on a batch of TRIGGER-stamped inputs.
    B: hidden activations on C_NEW inputs.
  Standardize -> PCA to PCA_DIM -> cap N_POINTS -> Rips persistence barcode.
  P(t) = sum of H0+H1 lifetimes (finite). Also track max-H1 lifetime.
* Checkpoint-index-as-filtration:
    baseline   = median P over the pre-injection window [0, K).
    threshold  = baseline + THRESH_K * (robust sigma of pre-injection P).
    birth step = first t (>=MIN_BIRTH) where P(t) > threshold AND stays
                 elevated (>= STAY_FRAC of the next STAY_WIN points also above).
    entrenchment   = final P (mean of last few checkpoints).
    staging speed  = #checkpoints from birth to first reaching 90% of final P.
    ring_width(t)  = |P(t) - P(t-1)|  (abruptness); spike at K reported.

OUTPUTS
-------
results.json, birth_vs_persistence.png, persistence_curves.png, ring_width.png,
VERDICT.md  (VERDICT.md is written by a separate step, not here).

Persistence backend: ripser (from ripser import ripser). gudhi is imported and
its version recorded for provenance / cross-check availability.
"""

import os
import json
import time
import warnings

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.datasets import load_digits
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from ripser import ripser
import gudhi  # imported for provenance / availability cross-check

warnings.filterwarnings("ignore")  # silence sklearn convergence chatter

# --------------------------------------------------------------------------- #
# Configuration                                                               #
# --------------------------------------------------------------------------- #
OUT_DIR = "/home/user/autoresearch-test/run31/m057_poc"
SCRATCH = "/tmp/run31/m057"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SCRATCH, exist_ok=True)

N_CKPT       = 30      # number of checkpoints (partial_fit passes)
K_INJECT     = 18      # TRUE late-injection step (1 .. N_CKPT-1)
SEEDS        = [0, 1, 2, 3, 4, 5, 6]   # >= 5 seeds
HIDDEN       = (64, 32)
LR           = 0.08
BATCH        = 256     # examples per partial_fit pass
POISON_FRAC  = 0.30    # fraction of batch replaced by triggers in RUN A (>=K)
TARGET_CLASS = 0       # backdoor target label
C_NEW        = 9       # held-out class introduced late in RUN B
TRIGGER_VAL  = 1.0     # max pixel after scaling to [0,1]
TRIG_CORNER  = 2       # 2x2 corner stamp

# concept-cloud / topology params
N_POINTS     = 150     # cap on points in the cloud
PCA_DIM      = 8       # reduce activations to this many dims before Rips
MAXDIM       = 1       # compute H0 and H1

# --- birth / change-point detection params --------------------------------- #
# IMPORTANT (empirical finding): introducing a late feature does NOT push the
# total persistence monotonically ABOVE baseline.  In this toy it triggers an
# abrupt RESTRUCTURING of the concept activation cloud (a large |dP| event) --
# the backdoor cloud COLLAPSES toward a tight target cluster (P falls) while the
# benign new-class cloud reorganizes and stays rich.  So the injection is dated
# from the dominant post-burn-in RING-WIDTH event (|P(t)-P(t-1)|), which is
# direction-agnostic, rather than from a sustained rise.
BURN_IN      = 6       # checkpoints of init transient to exclude from candidates
SMOOTH_W     = 3       # moving-average window for the ring-width signal
ONSET_FRAC   = 0.40    # birth = onset where smoothed ring rises to base+frac*(peak-base)
FINAL_WIN    = 4       # checkpoints averaged for "final P" (entrenchment)
RING_K_LO    = 1       # ring-spike window around K: [K-RING_K_LO, K+RING_K_HI]
RING_K_HI    = 5


# --------------------------------------------------------------------------- #
# Data helpers                                                                #
# --------------------------------------------------------------------------- #
def load_data():
    d = load_digits()
    X = d.data.astype(np.float64) / 16.0     # -> [0,1]
    y = d.target.astype(int)
    img_shape = (8, 8)
    return X, y, img_shape


def stamp_trigger(X, img_shape=(8, 8), corner=TRIG_CORNER, val=TRIGGER_VAL):
    """Return a copy of X with a corner x corner top-left block forced to `val`."""
    Xs = X.copy().reshape(-1, *img_shape)
    Xs[:, :corner, :corner] = val
    return Xs.reshape(X.shape)


def hidden_activations(clf, X):
    """Explicit forward pass to the LAST hidden layer (ReLU)."""
    A = X
    for i in range(len(clf.coefs_) - 1):           # stop before the output layer
        A = A @ clf.coefs_[i] + clf.intercepts_[i]
        A = np.maximum(A, 0.0)                      # ReLU (sklearn default)
    return A


# --------------------------------------------------------------------------- #
# Topology                                                                    #
# --------------------------------------------------------------------------- #
def total_persistence(points, rng):
    """
    Standardize -> PCA(PCA_DIM) -> cap N_POINTS -> Rips (ripser).
    Returns (P_total, max_H1) where:
        P_total = sum of finite H0 + H1 lifetimes
        max_H1  = largest finite H1 lifetime (0 if none)
    """
    pts = np.asarray(points, dtype=np.float64)
    if pts.shape[0] < 5:
        return 0.0, 0.0

    # subsample to cap size (reproducible)
    if pts.shape[0] > N_POINTS:
        idx = rng.choice(pts.shape[0], size=N_POINTS, replace=False)
        pts = pts[idx]

    # standardize then PCA
    pts = StandardScaler().fit_transform(pts)
    ncomp = min(PCA_DIM, pts.shape[1], pts.shape[0] - 1)
    if ncomp >= 2 and pts.shape[1] > ncomp:
        pts = PCA(n_components=ncomp, random_state=0).fit_transform(pts)

    dgms = ripser(pts, maxdim=MAXDIM)["dgms"]
    h0, h1 = dgms[0], dgms[1]

    h0_life = (h0[:, 1] - h0[:, 0])
    h0_life = h0_life[np.isfinite(h0_life)]        # drop the infinite component
    if h1.shape[0] > 0:
        h1_life = (h1[:, 1] - h1[:, 0])
        h1_life = h1_life[np.isfinite(h1_life)]
    else:
        h1_life = np.array([])

    P = float(h0_life.sum() + h1_life.sum())
    max_h1 = float(h1_life.max()) if h1_life.size else 0.0
    return P, max_h1


# --------------------------------------------------------------------------- #
# One full run (A or B) for one seed                                          #
# --------------------------------------------------------------------------- #
def run_one(mode, seed, X, y, img_shape):
    """
    mode: 'A' (backdoor) or 'B' (benign late capability).
    Returns dict with P_curve, maxh1_curve, and final test/backdoor accuracy.
    """
    rng = np.random.default_rng(1000 * seed + (0 if mode == "A" else 1))

    classes = np.arange(10)

    # --- split: keep a fixed pool for "concept" probing -------------------- #
    # benign training pool (mode B excludes C_NEW before K)
    full_idx = np.arange(len(X))

    # concept-probe sets (fixed across checkpoints for a clean filtration axis)
    trig_pool_idx = rng.choice(full_idx, size=N_POINTS, replace=False)
    X_trig_probe = stamp_trigger(X[trig_pool_idx], img_shape)   # for mode A cloud

    cnew_idx = np.where(y == C_NEW)[0]
    if len(cnew_idx) > N_POINTS:
        cnew_idx = rng.choice(cnew_idx, size=N_POINTS, replace=False)
    X_cnew_probe = X[cnew_idx]                                   # for mode B cloud

    clf = MLPClassifier(
        hidden_layer_sizes=HIDDEN,
        activation="relu",
        solver="adam",
        learning_rate_init=LR,
        max_iter=1,
        warm_start=True,
        random_state=seed,
    )

    P_curve, maxh1_curve = [], []

    for t in range(N_CKPT):
        # ----- assemble the training batch for this checkpoint ------------- #
        bidx = rng.choice(full_idx, size=BATCH, replace=True)
        Xb, yb = X[bidx].copy(), y[bidx].copy()
        sw = np.ones(BATCH, dtype=float)

        if mode == "B":
            # benign: withhold C_NEW from the LEARNING SIGNAL before K via a
            # zero sample-weight gradient mask, then introduce it at full
            # weight from K onward.  (Class set stays constant for warm_start.)
            if t < K_INJECT:
                sw[yb == C_NEW] = 0.0
        else:  # mode A backdoor
            if t >= K_INJECT:
                npois = int(POISON_FRAC * BATCH)
                pidx = rng.choice(BATCH, size=npois, replace=False)
                Xb[pidx] = stamp_trigger(Xb[pidx], img_shape)
                yb[pidx] = TARGET_CLASS

        clf.partial_fit(Xb, yb, classes=classes, sample_weight=sw)

        # ----- build the concept cloud & measure persistence --------------- #
        if mode == "A":
            cloud = hidden_activations(clf, X_trig_probe)
        else:
            cloud = hidden_activations(clf, X_cnew_probe)

        P, mh1 = total_persistence(cloud, rng)
        P_curve.append(P)
        maxh1_curve.append(mh1)

    # ----- end-of-training diagnostics ------------------------------------ #
    pred = clf.predict(X)
    test_acc = float((pred == y).mean())

    if mode == "A":
        # backdoor attack-success-rate on non-target inputs
        nt = y != TARGET_CLASS
        Xt = stamp_trigger(X[nt], img_shape)
        asr = float((clf.predict(Xt) == TARGET_CLASS).mean())
        extra = {"backdoor_asr": asr}
    else:
        # recall on the late-introduced class
        m = y == C_NEW
        rec = float((clf.predict(X[m]) == C_NEW).mean())
        extra = {"cnew_recall": rec}

    return {
        "P_curve": np.asarray(P_curve, dtype=float),
        "maxh1_curve": np.asarray(maxh1_curve, dtype=float),
        "test_acc": test_acc,
        **extra,
    }


# --------------------------------------------------------------------------- #
# Birth / entrenchment / staging from a P(t) curve                            #
# --------------------------------------------------------------------------- #
def robust_sigma(x):
    """MAD-based robust standard-deviation estimate."""
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    return 1.4826 * mad


def _smooth(x, w=SMOOTH_W):
    if w <= 1:
        return np.asarray(x, float)
    return np.convolve(np.asarray(x, float), np.ones(w) / w, mode="same")


def analyze_curve(P):
    """
    Date the injection from the dominant post-burn-in restructuring of P(t).

    ring_width(t) = |P(t)-P(t-1)|  (index in diff-space i corresponds to the
    transition P[i]->P[i+1]; we map an event culminating there to checkpoint i+1).

    Steps:
      * smooth ring_width
      * candidates = post-burn-in transitions (>= BURN_IN)
      * steady baseline/sigma = ring stats over [BURN_IN, K)  (pre-injection,
        post-init) -- used only for reporting / a sanity threshold
      * peak = argmax of smoothed ring over candidates  (the staging climax)
      * birth = onset: walking back from peak, the first checkpoint where the
        smoothed ring rises through  base + ONSET_FRAC*(peak-base)
      * staging_speed = peak - birth  (checkpoints from onset to climax;
        SMALLER = faster / more abrupt)
      * final_P = mean of last FINAL_WIN checkpoints (entrenchment, as specified)
      * dip_depth = mean P over [BURN_IN,K) minus min P over [K, end]
                    (how far the cloud collapsed after injection)
      * ring_spike_at_K = max ring_width in [K-RING_K_LO, K+RING_K_HI]
    """
    P = np.asarray(P, dtype=float)
    ring = np.abs(np.diff(P))                       # length N_CKPT-1
    rs = _smooth(ring)

    steady = rs[BURN_IN:K_INJECT - 1]               # pre-injection, post-burn-in
    if steady.size == 0:
        steady = rs[:K_INJECT - 1]
    base = float(np.median(steady))
    sigma = max(float(robust_sigma(steady)), 1e-9)
    threshold = base + 2.5 * sigma                  # reported sanity threshold

    cand = np.arange(BURN_IN, len(rs))
    if cand.size == 0:
        cand = np.arange(len(rs))
    peak_i = int(cand[np.argmax(rs[cand])])         # diff-space index of climax
    peak_val = float(rs[peak_i])

    level = base + ONSET_FRAC * (peak_val - base)
    onset_i = BURN_IN
    for i in range(peak_i, BURN_IN - 1, -1):
        if rs[i] < level:
            onset_i = i + 1
            break
    else:
        onset_i = BURN_IN

    birth = onset_i + 1                             # diff-index -> checkpoint
    peak_ck = peak_i + 1
    birth = int(min(birth, N_CKPT - 1))
    peak_ck = int(min(peak_ck, N_CKPT - 1))
    staging = int(max(peak_ck - birth, 0))          # onset -> climax span

    final_P = float(np.mean(P[-FINAL_WIN:]))
    pre_mean = float(np.mean(P[BURN_IN:K_INJECT]))
    post_min = float(np.min(P[K_INJECT:]))
    dip_depth = float(pre_mean - post_min)

    lo = max(0, K_INJECT - RING_K_LO - 1)
    hi = min(len(ring), K_INJECT + RING_K_HI - 1)
    ring_spike_at_K = float(np.max(ring[lo:hi])) if hi > lo else 0.0

    return {
        "baseline_ring": base,
        "sigma_ring": sigma,
        "threshold_ring": threshold,
        "birth": birth,
        "peak_checkpoint": peak_ck,
        "peak_ring": peak_val,
        "final_P": final_P,
        "pre_mean_P": pre_mean,
        "post_min_P": post_min,
        "dip_depth": dip_depth,
        "staging_speed": staging,
        "ring_width": ring.tolist(),
        "ring_spike_at_K": ring_spike_at_K,
    }


# --------------------------------------------------------------------------- #
# Plotting                                                                     #
# --------------------------------------------------------------------------- #
def make_plots(agg, out_dir):
    tA = np.arange(N_CKPT)

    # 1) persistence curves (mean +/- std), K marked -----------------------
    plt.figure(figsize=(8, 5))
    for mode, color in (("A", "crimson"), ("B", "steelblue")):
        M = np.array(agg[mode]["P_curves"])      # seeds x N_CKPT
        mu, sd = M.mean(0), M.std(0)
        lbl = "A: backdoor (trigger->target)" if mode == "A" else "B: benign late class"
        plt.plot(tA, mu, color=color, label=lbl, lw=2)
        plt.fill_between(tA, mu - sd, mu + sd, color=color, alpha=0.18)
    plt.axvline(K_INJECT, color="k", ls="--", lw=1.5, label=f"TRUE K = {K_INJECT}")
    plt.xlabel("checkpoint t (filtration axis)")
    plt.ylabel("total persistence  P(t) = sum H0+H1 lifetimes")
    plt.title("M057: concept-cloud persistence over the checkpoint timeline")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "persistence_curves.png"), dpi=130)
    plt.close()

    # 2) birth vs entrenchment scatter (per seed) --------------------------
    plt.figure(figsize=(7, 5.5))
    for mode, color, mk in (("A", "crimson", "o"), ("B", "steelblue", "s")):
        births = [b for b in agg[mode]["births"] if b is not None]
        finals = [agg[mode]["finals"][i] for i, b in enumerate(agg[mode]["births"]) if b is not None]
        jitter = (np.random.default_rng(7).standard_normal(len(births)) * 0.06)
        lbl = "A: backdoor" if mode == "A" else "B: benign"
        plt.scatter(np.array(births) + jitter, finals, c=color, marker=mk,
                    s=70, edgecolor="k", label=lbl, alpha=0.85)
    plt.axvline(K_INJECT, color="k", ls="--", lw=1.2, label=f"TRUE K = {K_INJECT}")
    plt.xlabel("recovered birth step")
    plt.ylabel("entrenchment (final P)")
    plt.title("M057: load-bearing-yet-young?  birth vs entrenchment")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "birth_vs_persistence.png"), dpi=130)
    plt.close()

    # 3) ring-width curves (mean), K marked --------------------------------
    tD = np.arange(1, N_CKPT)
    plt.figure(figsize=(8, 5))
    for mode, color in (("A", "crimson"), ("B", "steelblue")):
        R = np.array(agg[mode]["ring_widths"])   # seeds x (N_CKPT-1)
        mu = R.mean(0)
        lbl = "A: backdoor" if mode == "A" else "B: benign"
        plt.plot(tD, mu, color=color, label=lbl, lw=2, marker=".")
    plt.axvline(K_INJECT, color="k", ls="--", lw=1.5, label=f"TRUE K = {K_INJECT}")
    plt.xlabel("checkpoint t")
    plt.ylabel("ring width |P(t) - P(t-1)|  (abruptness)")
    plt.title("M057: staging abruptness around the injection step")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "ring_width.png"), dpi=130)
    plt.close()


# --------------------------------------------------------------------------- #
# Main                                                                         #
# --------------------------------------------------------------------------- #
def main():
    t_start = time.time()
    X, y, img_shape = load_data()
    print(f"[data] load_digits X={X.shape} classes={len(np.unique(y))} "
          f"pixels in [{X.min():.1f},{X.max():.1f}]")
    print(f"[cfg ] N_CKPT={N_CKPT} K_INJECT={K_INJECT} seeds={SEEDS} "
          f"hidden={HIDDEN} backend=ripser (gudhi {gudhi.__version__} available)")

    per_seed = []
    agg = {
        "A": {"P_curves": [], "ring_widths": [], "births": [], "finals": []},
        "B": {"P_curves": [], "ring_widths": [], "births": [], "finals": []},
    }

    for seed in SEEDS:
        rec = {"seed": seed}
        for mode in ("A", "B"):
            run = run_one(mode, seed, X, y, img_shape)
            ana = analyze_curve(run["P_curve"])

            agg[mode]["P_curves"].append(run["P_curve"].tolist())
            agg[mode]["ring_widths"].append(ana["ring_width"])
            agg[mode]["births"].append(ana["birth"])
            agg[mode]["finals"].append(ana["final_P"])

            err = (abs(ana["birth"] - K_INJECT) if ana["birth"] is not None else None)
            rec[mode] = {
                "birth": ana["birth"],
                "abs_err": err,
                "peak_checkpoint": ana["peak_checkpoint"],
                "final_P": ana["final_P"],
                "pre_mean_P": ana["pre_mean_P"],
                "post_min_P": ana["post_min_P"],
                "dip_depth": ana["dip_depth"],
                "baseline_ring": ana["baseline_ring"],
                "threshold_ring": ana["threshold_ring"],
                "staging_speed": ana["staging_speed"],
                "ring_spike_at_K": ana["ring_spike_at_K"],
                "test_acc": run["test_acc"],
            }
            if mode == "A":
                rec[mode]["backdoor_asr"] = run["backdoor_asr"]
            else:
                rec[mode]["cnew_recall"] = run["cnew_recall"]

        per_seed.append(rec)
        print(f"[seed {seed}] "
              f"A: birth={rec['A']['birth']} err={rec['A']['abs_err']} "
              f"finalP={rec['A']['final_P']:.2f} stage={rec['A']['staging_speed']} "
              f"asr={rec['A']['backdoor_asr']:.2f}  |  "
              f"B: birth={rec['B']['birth']} err={rec['B']['abs_err']} "
              f"finalP={rec['B']['final_P']:.2f} stage={rec['B']['staging_speed']} "
              f"rec={rec['B']['cnew_recall']:.2f}")

    # ----- aggregate ------------------------------------------------------- #
    def collect(mode, key):
        return [s[mode][key] for s in per_seed if s[mode][key] is not None]

    def stats(vals):
        if len(vals) == 0:
            return {"n": 0, "mean": None, "std": None, "median": None,
                    "min": None, "max": None}
        a = np.asarray(vals, dtype=float)
        return {"n": int(a.size), "mean": float(a.mean()), "std": float(a.std()),
                "median": float(np.median(a)), "min": float(a.min()),
                "max": float(a.max())}

    aggregate = {}
    for mode in ("A", "B"):
        aggregate[mode] = {
            "birth": stats(collect(mode, "birth")),
            "abs_err": stats(collect(mode, "abs_err")),
            "within2_count": int(sum(1 for s in per_seed
                                     if s[mode]["abs_err"] is not None
                                     and s[mode]["abs_err"] <= 2)),
            "final_P": stats(collect(mode, "final_P")),
            "dip_depth": stats(collect(mode, "dip_depth")),
            "staging_speed": stats(collect(mode, "staging_speed")),
            "ring_spike_at_K": stats(collect(mode, "ring_spike_at_K")),
            "test_acc": stats(collect(mode, "test_acc")),
            "n_births_detected": int(sum(1 for s in per_seed if s[mode]["birth"] is not None)),
        }
    aggregate["A"]["backdoor_asr"] = stats(collect("A", "backdoor_asr"))
    aggregate["B"]["cnew_recall"] = stats(collect("B", "cnew_recall"))

    # within-seed paired contrasts (A minus B)
    paired = {"staging_A_minus_B": [], "final_A_minus_B": [],
              "dip_A_minus_B": [], "ringspike_A_minus_B": [], "birth_A_minus_B": []}
    for s in per_seed:
        paired["staging_A_minus_B"].append(s["A"]["staging_speed"] - s["B"]["staging_speed"])
        paired["final_A_minus_B"].append(s["A"]["final_P"] - s["B"]["final_P"])
        paired["dip_A_minus_B"].append(s["A"]["dip_depth"] - s["B"]["dip_depth"])
        paired["ringspike_A_minus_B"].append(s["A"]["ring_spike_at_K"] - s["B"]["ring_spike_at_K"])
        paired["birth_A_minus_B"].append(s["A"]["birth"] - s["B"]["birth"])
    paired_stats = {k: stats(v) for k, v in paired.items()}

    # ----- plots ----------------------------------------------------------- #
    make_plots(agg, OUT_DIR)
    print(f"[plot] wrote persistence_curves.png, birth_vs_persistence.png, ring_width.png")

    # ----- assemble results.json ------------------------------------------ #
    results = {
        "model": "M057 Persistent-Homology Bruise Forensics (CPU PoC)",
        "backend_persistence": "ripser",
        "gudhi_version_available": gudhi.__version__,
        "config": {
            "N_CKPT": N_CKPT, "K_INJECT_true": K_INJECT, "seeds": SEEDS,
            "hidden": list(HIDDEN), "lr": LR, "batch": BATCH,
            "poison_frac": POISON_FRAC, "target_class": TARGET_CLASS,
            "c_new": C_NEW, "trigger_corner": TRIG_CORNER, "n_points": N_POINTS,
            "pca_dim": PCA_DIM, "maxdim": MAXDIM,
        },
        "definitions": {
            "P(t)": "sum of finite H0 + H1 lifetimes of the Rips barcode of the standardized/PCA'd concept activation cloud (ripser, maxdim=1)",
            "concept_cloud_A": "last-hidden-layer activations on a fixed batch of TRIGGER-stamped inputs",
            "concept_cloud_B": "last-hidden-layer activations on a fixed batch of class-C_NEW inputs",
            "ring_width(t)": "|P(t)-P(t-1)|, smoothed with a width-%d moving average for detection" % SMOOTH_W,
            "burn_in": f"first {BURN_IN} checkpoints (init transient) excluded from birth candidates",
            "baseline_ring": "median smoothed ring-width over the steady pre-injection window [BURN_IN, K)",
            "peak_checkpoint": "checkpoint of the dominant (max) smoothed ring-width event among candidates >= BURN_IN (staging climax)",
            "birth": f"ONSET of that dominant event: walking back from the peak, first checkpoint where smoothed ring rises through base + {ONSET_FRAC}*(peak-base). Direction-agnostic (works whether P rises or falls).",
            "entrenchment_final_P": f"mean of P over the last {FINAL_WIN} checkpoints (as specified). NOTE: a backdoor COLLAPSES its cloud, so final_P is LOW even though the feature is load-bearing.",
            "dip_depth": "mean P over [BURN_IN,K) minus min P over [K,end]: how far the concept cloud collapsed after injection",
            "staging_speed": "peak_checkpoint - birth = #checkpoints from onset to climax of the restructuring; SMALLER = faster / more abrupt",
            "ring_spike_at_K": f"max raw ring_width in window [K-{RING_K_LO}, K+{RING_K_HI}]",
            "DESIGN_NOTE": "Empirically the late feature does NOT raise total persistence above baseline; it triggers an abrupt RESTRUCTURING. Backdoor (trigger->one target) collapses the cloud (P falls, low final_P); benign new class enriches it (P dips then recovers, high final_P). Birth is therefore dated from the |dP| change-point, not a sustained rise.",
        },
        "per_seed": per_seed,
        "aggregate": aggregate,
        "paired_A_minus_B": paired_stats,
        "runtime_sec": round(time.time() - t_start, 1),
    }

    # numpy-safe JSON
    def default(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(str(type(o)))

    with open(os.path.join(OUT_DIR, "results.json"), "w") as f:
        json.dump(results, f, indent=2, default=default)

    # ----- console summary ------------------------------------------------- #
    print("\n================ AGGREGATE SUMMARY ================")
    print(f"runtime: {results['runtime_sec']} s")
    print(f"backend: ripser   (gudhi {gudhi.__version__} also available)")
    print(f"TRUE injection step K = {K_INJECT}")
    for mode, name in (("A", "BACKDOOR"), ("B", "BENIGN  ")):
        ag = aggregate[mode]
        print(f"\n[{name}]")
        print(f"  recovered birth : mean={ag['birth']['mean']:.2f} "
              f"median={ag['birth']['median']} (true K={K_INJECT})")
        print(f"  |birth - K|     : mean={ag['abs_err']['mean']:.2f} "
              f"median={ag['abs_err']['median']} max={ag['abs_err']['max']:.0f}  "
              f"within +/-2: {ag['within2_count']}/{len(SEEDS)}")
        print(f"  entrenchment P  : mean={ag['final_P']['mean']:.2f} "
              f"+/- {ag['final_P']['std']:.2f}  (final P)")
        print(f"  dip depth       : mean={ag['dip_depth']['mean']:.2f} "
              f"+/- {ag['dip_depth']['std']:.2f}  (collapse magnitude)")
        print(f"  staging speed   : mean={ag['staging_speed']['mean']:.2f} "
              f"median={ag['staging_speed']['median']} (smaller=faster/abrupt)")
        print(f"  ring spike @K   : mean={ag['ring_spike_at_K']['mean']:.2f}")
    print(f"\n[A backdoor ASR ] mean={aggregate['A']['backdoor_asr']['mean']:.3f}")
    print(f"[B C_NEW recall ] mean={aggregate['B']['cnew_recall']['mean']:.3f}")
    print("\n[PAIRED  A - B  (within seed)]")
    for k, v in paired_stats.items():
        print(f"  {k:24s}: mean={v['mean']} std={v['std']} n={v['n']}")
    print("===================================================")
    print(f"\nWrote: {OUT_DIR}/results.json and 3 PNGs")
    return results


if __name__ == "__main__":
    main()
