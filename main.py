# SINGLE-STEP APPROACH (what most people do)
def simple_qa(question):
    """Just ask the LLM directly"""
    response = llm.generate(f"Answer this question: {question}")
    return response

# Result: Often hallucinated or wrong answers for complex questions


# PROGRAM-LEVEL REASONING CHAIN (DSPy approach)
import dspy

class ResearchAssistant(dspy.Module):
    """Multi-step reasoning program for complex questions"""
    
    def __init__(self):
        # Step 1: Break down complex question
        self.decomposer = dspy.ChainOfThought("question -> sub_questions: List[str]")
        
        # Step 2: Retrieve relevant information
        self.retriever = dspy.Retrieve(k=5)
        
        # Step 3: Synthesize information
        self.synthesizer = dspy.ChainOfThought("context, question -> reasoning, answer")
        
        # Step 4: Verify answer quality
        self.verifier = dspy.ChainOfThought("question, answer -> confidence_score: float, issues: List[str]")

    def forward(self, question):
        # CHAIN STEP 1: Decompose question
        breakdown = self.decomposer(question=question)
        
        # CHAIN STEP 2: Research each sub-question
        all_context = []
        for sub_q in breakdown.sub_questions:
            docs = self.retriever(sub_q)
            all_context.extend(docs)
        
        # CHAIN STEP 3: Synthesize answer
        synthesis = self.synthesizer(
            context=" ".join(all_context), 
            question=question
        )
        
        # CHAIN STEP 4: Self-verification
        verification = self.verifier(
            question=question, 
            answer=synthesis.answer
        )
        
        # CHAIN STEP 5: Decide whether to retry or return
        if verification.confidence_score < 0.7:
            # Retry with different approach or ask for clarification
            return self.fallback_strategy(question, verification.issues)
        
        return dspy.Prediction(
            answer=synthesis.answer,
            reasoning=synthesis.reasoning,
            confidence=verification.confidence_score,
            sources=all_context[:3]
        )

# EXAMPLE USAGE
assistant = ResearchAssistant()

question = "What are the economic impacts of climate change on small island nations?"

# This creates a REASONING CHAIN:
# 1. "What are small island nations?" + "What economic sectors exist there?" + "How does climate change affect each?"
# 2. Retrieve academic papers, reports, case studies
# 3. Synthesize: "Tourism revenue drops 40% from beach erosion, fishing industry..."  
# 4. Verify: "High confidence (0.85) - well-supported by multiple sources"
# 5. Return comprehensive, sourced answer

result = assistant(question)


# WHAT ARBOR OPTIMIZES IN THIS CHAIN:
# Traditional approach: Optimize each step separately
# Arbor approach: Optimize THE ENTIRE CHAIN end-to-end

# For example, through RL, Arbor might learn:
# - Better question decomposition strategies
# - Which types of sources to prioritize
# - How to weight different pieces of evidence  
# - When to be confident vs. when to hedge
# - How to structure reasoning for clarity

# The reward signal teaches the WHOLE PROGRAM to work better together


# COMPARISON WITH SIMPLE APPROACH:
simple_answer = simple_qa(question)
# Result: "Climate change affects island economies through rising sea levels..."
# Issues: Vague, potentially inaccurate, no sources, no reasoning shown

program_answer = assistant(question)  
# Result: Detailed analysis with specific data points, clear reasoning, source citations, confidence scores
