# Life Analogy — Persian ney 4-register overblowing with interdental embouchure null-mode transitions

The **Persian ney** (نى):
- 4 registers: **bam** (fundamental) + **zir** (octave) + **geesh** (octave + 5th) + **pas-geesh** (2 octaves); skilled neyzen reaches 3+ octaves.
- Interdental technique: rim slightly between front teeth + tongue air-direction (Turkoman late-1700s lineage).
- Register transition: air velocity + embouchure micro-adjustment defines the null pressure-mode that selects which harmonic dominates; between registers there's a brief "null gate" where neither register sounds — the air is in transition.
- Quarter-tones via partial hole covering between registers.

**NEY-4-REGISTER-NULL-GATE-OVERBLOW-PROJECTION**: per-task gradient null-space projection with 4-register hierarchy + register-transition null-gate + breath-velocity scheduler + partial-hole quarter-tone interpolation. (1) **4-register hierarchical null-spaces** N_bam ⊂ N_zir ⊂ N_geesh ⊂ N_pasgeesh: each higher register is a refinement of the lower one's null-space; new task gradient projected onto the lowest still-permitted null-space. (2) **Register-transition null-gate** G_trans: when projection magnitude exceeds register's tau_R, force transition to next-higher register (analogous to neyzen overblowing); a brief null-update step (zero update) is enforced during transition to mimic the null-pressure gate. (3) **Breath-velocity scheduler v_breath**: training-step LR proportional to gradient projection magnitude; high-velocity transitions correspond to higher registers. (4) **Partial-hole quarter-tone interpolation**: between registers, allow fractional projection onto a 0.5-weighted-sum subspace (analogous to neyzen partial fingering) for quarter-tone task interpolation. (5) **Interdental embouchure control** = soft-thresholding on gradient: only above tau_emb does the projection apply. (6) Differs from R414 + R427 + R441 + R453 + R469 + R478 + R491 + R503 (null-space-LoRA continuous-time melisma gradient rubato) by 4-register hierarchical null-space + register-transition null-gate + breath-velocity LR scheduler + partial-hole quarter-tone interpolation.

## Adjacency
- GNSP Gradient Null-Space Projection VLM 2507.19839
- GORP Continual Gradient Low-Rank Projection 2507.02503
- SubTrack++ Gradient Subspace Tracking
- Continual Gradient Low-Rank Projection ACL 2025

Expected FAIL — gradient null-space projection + continual learning + subspace tracking literature covers.
