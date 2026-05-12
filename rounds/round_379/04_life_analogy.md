# Life Analogy — Andean Inca quipu (khipu)

The **quipu** is the Inca knotted-cord administrative record system:
- Main cord (horizontal) with **pendant cords** hanging off it.
- Each pendant carries **knots at positions** representing base-10 places (1s, 10s, 100s, …) from bottom (lowest) to top.
- **Color** of each pendant = category of information (e.g., census, livestock, tribute).
- **Knot type** (single overhand, figure-of-eight, granny) = specific values.
- **Subsidiary pendant cords** branch off pendants for secondary/tertiary detail.
- **Spacing between knot clusters** separates place values (e.g., 45 vs 405).
- **Twist direction** (left/right) and **fiber type** carry additional dimensions.
- Reading required trained **quipucamayocs** specialists.

The unique principle: **multi-dimensional encoding via position-color-spacing-twist-knot-type combinatorial channels**, with **explicit hierarchical place-value structure** (decimal radix; subsidiary cords as exceptions).

## Analogical mapping → LLM external memory

- Main cord ↔ root memory pointer (top-level memory index)
- Pendant cord ↔ second-level memory cluster
- Color ↔ category embedding
- Knot position on pendant ↔ position-encoded place value
- Subsidiary pendant ↔ third-level memory branch (exception/correction)
- Twist direction ↔ orthogonal dimension (e.g., recency vs salience)
- Quipucamayoc ↔ retrieval policy

The mechanism: a **multi-dimensional hierarchical key encoding** for external LLM memory where each memory entry carries (i) a base-K positional code (digits 0..K-1 at depth d), (ii) a color-category embedding, (iii) a spacing field (separator marker), (iv) a twist-binary flag (e.g., recency vs salience). Retrieval uses a **combinatorial-channel filter**: query specifies any subset of channels and the system returns all entries matching that subset. Differs from H-MEM (single positional index per memory layer) by encoding *multiple orthogonal* channels per entry and supporting *partial-channel retrieval* (e.g., "all category=red memories regardless of position").
