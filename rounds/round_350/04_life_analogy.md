# R350 — life analogy

## Source: Mongolian recurve composite bow
- Bamboo wood core + horn (compression-strong) belly + sinew (tension-strong) back.
- Layered laminate: each layer optimal for one stress direction.
- Glue binds opposing stress responses into single member.
- Years of construction; far higher draw weight per unit length than self-bow.

## LLM analogy
**LAMINATE-INIT**: weight initialization with EXPLICIT laminate structure — different layers initialized with different distributions optimized for different stress directions. Weights with predominant POSITIVE gradient flow get heavy-tail (sinew/tension) initialization; weights with predominant NEGATIVE gradient flow get bounded (horn/compression) initialization. Initialization is INFORMED BY estimated gradient-flow direction at each weight position.

## Differs from prior art (claim)
Standard weight init (Xavier/He/Kaiming) is direction-agnostic. Layer-wise init (DS-Init, DeepNet) scales by depth. LAMINATE-INIT differs by USING GRADIENT-FLOW-DIRECTION-INFORMED init with two distinct distribution families for tension-vs-compression weight roles — composite-laminate-style structural initialization.
