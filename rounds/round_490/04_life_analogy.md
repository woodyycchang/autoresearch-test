# Life Analogy — Greek bouzouki tetrachord 4-course coupling

The **bouzouki tetrachordo** (Greek):
- 4 paired courses (8 strings total).
- Lower 2 courses octave-paired (C3+C4, F3+F4); upper 2 unison (A3+A3, D4+D4).
- Player strikes pair simultaneously → coupled-string phase coherence enhances tone.
- 4-course CFAD tuning establishes harmonic mode.

**BOUZOUKI-TETRACHORD-COUPLE**: 4-course paired-attention-head coupling for KV cache compression + phase-coherent stereo-pair lookup. (1) Group 4 attention heads into 2 octave-pairs + 2 unison-pairs (4 total pair-courses). (2) Octave-pairs: head_h1 + head_h2 share K_h1 but have V_h1, V_h2 at different scales (octave 2x scaling). (3) Unison-pairs: heads share both K, V (paired duplicate). (4) Phase coherence: per-pair K,V outputs averaged with phase-locked weight. (5) Result: KV cache reduced by ~50% via course-pairing while preserving 4-mode tetrachord harmonic structure.

## Adjacency
- DeepSeek MLA shared latent (ACL 2025)
- CLA Cross-Layer KV sharing
- MTLA Temporal Latent Attention
- GQA Grouped Query Attention

Expected FAIL — KV pair-sharing across heads/layers paradigm covered.
