# R683 motivation

Cantor middle-thirds set: start with [0,1], remove middle third → take
[0,1/3]∪[2/3,1], recurse. Limit set has Hausdorff dimension log2/log3
≈ 0.631. Self-similar fractal structure.

For LR schedule: at each level, place LR-active intervals on Cantor
subintervals, LR-plateau on removed middle thirds. Recursion to depth
d gives 2^d active intervals each of size 3^-d.

Motivation: mechanism_transfer (Cantor construction is precise).
Pre-existing fractal-LR literature (Agarwal 2021) overlaps but uses
Chebyshev step-size fractal not Cantor self-similar.
