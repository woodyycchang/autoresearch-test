# R249 — life analogy

## Source domain: whitewater rafting eddy-hopping
- A river has DANGEROUS HYDRAULICS (drops, holes, strainers) and SAFE EDDIES (calm slack water behind obstacles).
- Eddy-hopping is the discipline of paddling from eddy to eddy: in each eddy, the paddler PAUSES, SCOUTS THE NEXT REACH, then ferry-angles across the current to the next eddy.
- Ferry angle = the boat's heading relative to current; controls lateral motion without losing downstream position.
- Never run a long unfamiliar reach without an eddy plan. Eddies are the SAFE-CHECKPOINTS of the river.

## LLM analogy candidate
**Eddy-hopping agent execution**: an LLM agent in a multi-step task does not flow continuously through the action sequence. Instead, it explicitly PAUSES at every K-th action in a SAFE-CHECKPOINT EDDY: a sandboxed scratchpad where the agent (a) snapshots the current state, (b) scouts the next K actions by hypothetical-execution, (c) evaluates the downstream consequences against safety constraints, (d) if safe, ferries forward; if not, returns to prior eddy. The eddy is a checkpoint where the agent can ALWAYS BACK OUT without committing the next K actions. Distinct from continuous CoT: forced periodic pauses with formal back-out option at each eddy.

## What differs from prior art (claim)
Four-Checkpoint Framework (2602.09629) defines safety checkpoints at fixed PIPELINE POSITIONS (CP1-CP4). MAGE Shadow Memory (2605.03228) addresses attention dilution. AgentSpec (2503.18666) is runtime enforcement spec. None propose periodic AGENT-INITIATED eddy-pauses with hypothetical-execution scouting and formal back-out option. The eddy-hopping discipline of "always pause before commit, with cheap back-out" is distinguishing.
