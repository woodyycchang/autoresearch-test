# R634 step 01

**Timestamp:** 2026-05-19T19:34:55Z

## Scan focus
Kernelized Stein discrepancy (KSD) as a mechanism source for evaluation-diagnostic. KSD provides a closed-form, sample-based test for whether a sample comes from a target distribution with known score function ∇log p. The candidate transfers KSD as a per-prompt evaluation tool: given an LLM's distribution over generations, test conformance to a target reference distribution via KSD with score function derivable from log-probabilities.

## Motivation
mechanism_transfer: KSD is a rigorous integral probability metric with closed-form U-statistic estimator. Recent Stein-LLM works (StainNet, SVGD-LLM) use Stein methods for sampling, but using KSD as a per-prompt evaluation diagnostic is less common.
