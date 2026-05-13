# Life Analogy — Hopi snake dance three-role grasp protocol

The **Hopi snake dance** uses a **three-role coordination protocol** for handling live rattlesnakes:
- **Carrier** holds snake in mouth (the high-risk operator).
- **Hugger** stands behind, arm on Carrier's shoulder, wielding a snake-whip to prevent coiling.
- **Gatherer** follows behind to retrieve dropped snakes before they reach the audience.

Each snake travels through the trio: gatherer → carrier → hugger collaborate per snake. The roles are **specialised and complementary** with strict task boundaries:
- Carrier MUST NOT release snake until safe drop point
- Hugger MUST keep snake from coiling around carrier
- Gatherer MUST contain accidents

The unique principle: **3-role specialisation with strict boundaries and complementary safety checks** for handling high-risk objects.

## Analogical mapping → LLM safe-tool-use agent

- Snake ↔ high-risk tool call (e.g., file write, irreversible API)
- Carrier ↔ tool-executor agent (performs action)
- Hugger ↔ active-constraint agent (continuously monitors call parameters; blocks unsafe coiling)
- Gatherer ↔ post-hoc cleanup agent (rolls back / contains accidental side effects)

The mechanism: a **3-role specialised tool-call protocol** for safety-critical agent actions. For each high-risk tool call, three sibling sub-agents coordinate: (1) EXECUTOR produces the tool-call request; (2) CONSTRAINER continuously enforces a policy on the argument space — if argument drifts toward unsafe region, it intervenes pre-call; (3) CONTAINMENT runs post-call to roll back side effects if execution diverged. Each role has STRICT TASK BOUNDARIES (Executor cannot block, Constrainer cannot execute, Containment cannot pre-empt). Differs from typical debate / judge multi-agent (which all agree/disagree on the same task) by having ROLE-SPECIALISATION + STRICT BOUNDARIES + TEMPORAL SEQUENCING (pre-call constraint, in-call execute, post-call contain).
