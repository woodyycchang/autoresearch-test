# R240 — life analogy

## Source domain: elephant infrasound + seismic dual-channel
- Elephants communicate over LONG RANGES (10 km airborne, 32 km seismic) via low-frequency rumbles (<20 Hz) inaudible to most mammals.
- TWO PARALLEL CHANNELS: air (sound waves) and ground (seismic / surface waves). Same vocalisation propagates through both.
- Reception: foot pads with cartilaginous nodes detect seismic; ear constriction muscle dampens airborne to focus on seismic when needed.
- Specific cultural function: long-range family coordination — herd movement, predator warnings, mate-finding — without continuous proximity.

## LLM analogy candidate
**Dual-channel "infrasound" deployment-wide weight-state broadcast for LLM-fleet coordination**: in a multi-replica LLM deployment (cloud fleet of N identical-base models with N independent fine-tunes / system prompts / contexts), introduce a periodic LOW-FREQUENCY broadcast — every τ seconds, each replica emits a compact "rumble vector" summarising its current state (recent topic drift, alignment-drift estimate, hallucination-rate, refusal-rate over last K requests). The rumble vector is broadcast on TWO PARALLEL CHANNELS: (a) a fast in-cluster message bus (airborne), (b) a slow persistent log (seismic). Other replicas listen on BOTH channels but PRIORITISE the slow log when in-cluster bus is busy (analog: ear-canal constriction). Effect: deployment-wide soft coordination of replicas — when one replica reports drift, others adapt their refusal thresholds, all without any centralised coordinator. The "infrasound" frequency is far below request-level traffic, so the side-channel doesn't compete with request bandwidth.

## What differs from prior art (claim)
LLM-fleet coordination work (UAV LLM-MAS 2602.19534, Space-Air-Ground-Sea 2509.02540, Spectrum Access 2604.13132) addresses task-level coordination via fast message passing. None proposes a low-frequency, periodic, dual-channel rumble broadcast for soft alignment-drift coordination across an LLM replica fleet.
