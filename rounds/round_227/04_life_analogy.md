# R227 — life analogy

## Source domain: falconry hood
- A hood blocks ALL visual stimulus, putting the raptor in calm-receptive state ("what it cannot see it does not fear").
- Manning protocol: dark room → hood-on with no stimulus → hood off in dark with food reward → gradually raise ambient light → only later introduce moving stimuli, then human, then outdoor → eventually free-fly.
- The hood is a STIMULUS MASK, the dark-to-light schedule is the curriculum, and the food reward at unhood = positive reinforcement at the moment input becomes interpretable.

## LLM analogy candidate
A test-time "stimulus-mask anneal" for safety-critical input processing: incoming user input is FIRST processed under heavy attention masking (analog: hood — high masking ratio on visual/multimodal tokens, very high softmax temperature ≈ blindness) so the model commits to no aggressive action, only neutral acknowledgement. The mask is then slowly lifted (decreasing mask ratio, lowering temperature) over a budgeted number of internal "habituation passes" of the same input until the model can respond from a calm-receptive state. Crucially, hooding is applied at INFERENCE not training, on a per-input basis, and the schedule is parameterised by an input-risk estimate (high-risk inputs get more habituation passes). The mask is the program, the temperature schedule is the curriculum, and the eventual unmasking aligned with a low-energy commit point is the food reward.

## What differs from prior art (claim)
Curriculum learning (2601.21698, 2503.07065, 2508.01540) does this at TRAINING time, with curricula authored over the dataset. The bobbin-lace-hood-style framing is per-input, at INFERENCE, with the mask schedule conditioned on per-input risk; not present in surveyed curriculum work.
