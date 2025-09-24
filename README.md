# dspy-examples

Here's a concrete example showing the difference between single-step and program-level reasoning:**Key Insight**: Program-level reasoning chains are **multi-step workflows** where each step feeds into the next, and the entire sequence is optimized together.

**Real-World Examples**:

1. **Legal Research Bot**:
   - Parse legal question → Identify relevant law areas → Search case law → Analyze precedents → Draft response → Cite sources

2. **Medical Diagnosis Assistant**:
   - Gather symptoms → Ask clarifying questions → Cross-reference medical literature → Suggest tests → Interpret results → Recommend treatment

3. **Financial Analysis Tool**:
   - Extract company data → Calculate ratios → Compare to industry benchmarks → Analyze trends → Generate investment thesis → Risk assessment

**Why This Matters for Optimization**:

**Traditional approach**: Optimize each step independently
- Step 1: Make question decomposition better
- Step 2: Make retrieval better  
- Step 3: Make synthesis better

**Problem**: Steps might work against each other - better retrieval might retrieve more info than synthesis can handle.

**Arbor's approach**: Optimize the ENTIRE chain end-to-end
- The reward signal (final answer quality) propagates back through all steps
- Each component learns to work better with the others
- Example: Retriever learns to find info that synthesizer can actually use effectively

**Critical Difference**: It's not just chaining AI calls - it's creating AI programs where components co-evolve to work optimally together. Like training a sports team vs. training individual players separately.
