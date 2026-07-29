# Applied AI Documentation Assistant Model Card

## 1. System Overview

This system is a documentation assistant that helps users answer questions about a codebase using retrieved evidence rather than relying only on a general language model. It is designed to be helpful for onboarding, debugging, and understanding project documentation while staying cautious about uncertainty.

## 2. Limitations and Biases

The system has several important limitations:

- Its retrieval is keyword-based, so it can miss relevant answers when the wording is different from the source text.
- It can be biased toward the most obvious or frequently repeated documentation snippets, which may overshadow less prominent but still important details.
- It may give an incomplete answer if the documentation is thin or ambiguous.
- The system is not a substitute for human judgment in sensitive or high-stakes technical decisions.

## 3. Potential Misuse and Prevention

This AI could be misused if someone treated it as a guaranteed authority instead of a support tool. A developer might trust it to make a risky decision without checking the original documentation. To reduce that risk, the system is designed to refuse unsupported answers, provide evidence-based summaries, and fall back safely when it lacks sufficient context. It should be used as a guide, not as the final authority.

## 4. What Surprised Me During Testing

The most surprising result was that the assistant behaved much more reliably when it used retrieved evidence rather than free-form generation alone. I also noticed that the system handled unsupported questions better than expected once guardrails were added, which showed that careful design can improve trustworthiness even when the underlying model is not perfect.

## 5. Collaboration With AI During This Project

I used AI as a coding and planning partner throughout the project. One helpful suggestion was when the AI proposed a safer fallback strategy for when no Gemini API key was available; that helped me turn a brittle failure path into a more robust experience. One flawed suggestion was a proposed response pattern that appeared more polished but could have encouraged the assistant to answer confidently without enough evidence. I corrected that by making the system rely on retrieval and explicit refusal behavior instead.

## 6. Reliability and Testing Notes

The system was tested with automated unit tests covering retrieval and fallback behavior. The current results were strong: 4 out of 4 tests passed. The system also logs retrieval and generation events, which improves transparency when something goes wrong.

## 7. Responsible Use Guidance

When using this system, developers should verify any critical technical decision against the original documentation or source code. The assistant should be treated as a support tool for exploration and summarization, not as a complete authority.
