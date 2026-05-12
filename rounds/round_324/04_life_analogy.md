# R324 — life analogy

## Source: Wankel rotary engine
- Triangular rotor inside epitrochoidal housing forms 3 working chambers continuously.
- Each chamber goes through intake → compression → expansion → exhaust as rotor rotates.
- 3 power impulses per rotor revolution; continuous power without reciprocating piston.

## LLM analogy
**WANKEL-INFER**: 3-phase inference rotor. Attention computation partitioned into 3 chambers each in different phase (intake=new tokens, compression=KV update, expansion=attention computation, exhaust=residual emission); chambers rotate through sequence positions continuously. Pipeline-parallelized at chamber granularity for continuous throughput.

## Differs from prior art (claim)
Continuous batching does prefill+decode pipelining. Pipeline parallelism partitions layers across devices. SpinQuant uses rotation for quantization. WANKEL-INFER's 3-chamber phase rotation across sequence is a specific scheduling pattern — close to continuous batching with phase-aware chunking.
