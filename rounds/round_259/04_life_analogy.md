# R259 — life analogy

## Source domain: leafcutter ant attini fungal cultivation
- Three+ size castes of workers, each specialized:
  - **Largest (majors)**: colony defense.
  - **Medium**: cut and carry leaves to nest.
  - **Smaller**: process leaves — cut into smaller pieces, chew with saliva, treat with antibacterial secretions.
  - **Smallest (minims)**: tend fungal garden — implant masticated substrate, weed contaminants, harvest gongylidia.
- The substrate moves through a SIZE-GRADED ASSEMBLY LINE: each stage performed by ever-smaller workers.
- The fungus (Leucoagaricus gongylophorus) is the MUTUALIST: it digests cellulose the ants can't, and produces gongylidia (specialized nutrient-rich hyphal swellings) as the ants' food.
- The garden has an antimicrobial regime (ant-secreted antibiotics + Pseudonocardia symbionts on ants' cuticles) preventing pathogenic fungal invasion.

## LLM analogy candidate
**Size-graded specialist caste pipeline with mutualist substrate (SGSCP)**: a multi-agent LLM system in which (1) tasks pass through a SIZE-GRADED CASCADE: a sequence of specialists ranging from large-model (24B, defense/triage) down through medium-model (8B, cut/decompose into sub-tasks) to small-model (1B, process atomic units) to tiny-model (200M, garden-tend — i.e., refine final tokens). (2) Each stage gets PROGRESSIVELY-SHRUNK context/scope: large model sees full task; tiny model sees only its assigned atomic unit. (3) A separate **mutualist substrate-model** (a fine-tuned specialist on the task's substrate, NOT in the pipeline itself but consulted via inference API — analogue of Leucoagaricus) holds slow-changing domain knowledge that the pipeline ants don't carry. (4) **Antibiotic regime**: a contaminant-detection model patrols substrate to flag prompt-injection or off-distribution inputs entering the pipeline. Distinct from cascading inference: SGSCP requires the mutualist substrate-model AND the size-graded specialization AND the antibiotic patrol; cascading inference is a 2-stage routing.

## What differs from prior art (claim)
PublicAgent (2511.03023), Multi-Agent AutoML (2410.02958), MAS Orchestration Survey (2601.13671) cover multi-agent pipelines and role specialization but not size-graded model-scale assembly line + external mutualist substrate-model + antibiotic-regime contaminant patrol triad.
