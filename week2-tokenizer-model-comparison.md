# Week 2 Assignment: Hugging Face Hub Scavenger Hunt

**Graduate Extension Included**

## Overview

Same fields I walked through in Monday's demo: parameter count/size, architecture family, license, tokenizer/vocab size. Pick 3 models, record those fields, run a tokenizer comparison across languages, check context window against this week's reading, then write a short reflection tying it back to a real project decision.

*Same order I used in Monday's demo: parameter count/size near the top of the card, architecture family in the description, license in the metadata, tokenizer/vocab size in tokenizer_config.json (or just test the model directly in a tokenizer tool).*

## How to Submit

1. Fill out this file directly (replace the `_____` placeholders and bracketed instructions with your answers).
2. Commit this file to the same GitHub repo you created for Assignment 1, using this exact filename: `week2-tokenizer-model-comparison.md`.
3. Push your commit, then submit a link to the file as instructed for this course.

---

## Part 1: Choose 3 Models

1. Go to huggingface.co/models.
2. Pick 3 models that actually make a meaningful comparison — not three near-identical variants of the same model. At least 2 different organizations/families, ideally a mix of sizes (small under ~3B, mid-size, larger).
3. Pick based on your own interests. Got a project idea? Use models you'd actually consider for it.

## Part 2: Record Your Findings

Where to find each field, if you get stuck:
- **Parameter count / size** — near the top of the card, sometimes right in the model's name (e.g. "7B" = 7 billion parameters).
- **Architecture family** — in the description text, or config.json under "Files and Versions."
- **License** — shown as a tag near the top, and always in the YAML metadata block.
- **Tokenizer / vocab size** — check tokenizer_config.json or config.json under "Files and Versions" for vocab_size. Can't find it? Note "not published" — that's a useful observation on its own.

| Model | Link | Parameter count / size | Architecture family | License | Tokenizer / vocab size |
|---|---|---|---|---|---|
| Model 1: Llama-3.2-1B-Instruct | https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct | 1B| Llama(Transfermer Decoder)| Llama 3.2 Community License | 128,256 |
| Model 2: Qwen2.5-7B-Instruct | https://huggingface.co/Qwen/Qwen2.5-7B-Instruct | 8B | Qwen2.5 (RoPE, SwiGLU) | Apache 2.0 | 151,643 |
| Model 3: DeepSeek-V3 | https://huggingface.co/deepseek-ai/DeepSeek-V3 | 685B | DeepSeek-V3 (Mixture-of-Experts) | DeepSeek-V3(undwer MIT licence) | 129,280 |

## Part 3: Tokenizer Comparison Exercise

Use a tokenizer tool that supports multiple model families (tiktokenizer.vercel.app works) and test all 3 models with the same three inputs:

- **Test sentence (use this exact sentence for all 3 models):** "I love learning about artificial intelligence."
- **Language A:** translate the test sentence into a Latin-script European language — Spanish, French, German, whatever. Same translation across all 3 models.
- **Language B:** translate it into a non-Latin-script language — Japanese, Arabic, Korean, Hindi, your call. Same translation across all 3 models.

| Model | Test sentence tokens | Language A used | Language A tokens | Language B used | Language B tokens |
|---|---|---|---|---|---|
| Model 1 | 7 | French | 14 | Chinese | 10 |
| Model 2 | 7 | French | 15 | Chinese | 5 |
| Model 3 | 7 | French | 13 | Chinese | 7 |

## Part 4: Context Window Check

For each model, look up its context window — the max tokens it can handle in one request. Usually on the card or in the config file.

| Model | Context window (tokens) | Source (URL or where you found it) |
|---|---|---|
| Model 1 | 128k | https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct |
| Model 2 | 131,072 | https://huggingface.co/Qwen/Qwen2.5-7B-Instruct |
| Model 3 | 128k | https://huggingface.co/deepseek-ai/DeepSeek-V3 |

**Now do the math for at least one model:** Chapter 2 is roughly 62 pages. Using ~500–600 words/page and ~0.75 words/token, estimate the total token count. Would the whole reading fit in that model's context window in one API call, with room left for a response? Show your work and your conclusion.

> [62 pages × 550 average words/page = 34100 words;
   Given that 1 token is about 0.75workds, the total tokens = 34100/0.75 =45467 tokens are needed. 
   Therefore, the whole chapter will fit into 3 models' context window of 128K, leaving enough room (131072-45467 is more than 85000 tokens) for the model to generate a long and detailed response in a single API call]

## Part 5: Comparison Reflection (300–400 words)

Answer all four:

- What's the biggest difference between your 3 models — size, architecture, license, tokenizer, something else?
- If you had to pick one for a real project, which one and why? Don't just say "the biggest one" — factor in license restrictions and whether the project actually needs that much size.
- Would your pick change for a multilingual or cost-sensitive use case, based on what you found in Part 3? Why or why not?
- Would your pick change for a use case involving long documents (full reports, long transcripts), based on the context window math in Part 4? Why or why not?

> [
- What's the biggest difference between your 3 models — size, architecture, license, tokenizer, something else?
By comparing the 3 models, I found that the biggest differences among them are their parameter scales and their approach to language optimization. In terms of size, they span completely different tiers: Llama-3.2 is an ultra-lightweight 1B edge model; Qwen2.5-7B is an 8B desktop/server model, a powerful and highly capable mid-sized model; DeepSeek-V3 is a massive 685B cloud-scale system (Mixture-of-Experts architecture). This difference in parameter scale directly affects how they processing vocabulary. Qwen features greater optimization for non-Latin multilingual scripts with its massive 151K vocabulary, whereas Llama and DeepSeek utilize more compressed tokenizers (around 128K–129K) that are great for English efficiency. Also, their licenses create different legal boundaries; Qwen2.5's Apache 2.0 license offers the most permissive path for commercialization compared to Meta's custom community license.
- If you had to pick one for a real project, which one and why?
If I had to select one of these open-source models for a real-world engineering project alongside my primary foundation model setup (OpenAI), I would choose Qwen2.5-7B-Instruct. While DeepSeek-V3 offers unparalleled reasoning power, hosting a massive MoE model locally is impractical for standard development environments. Llama-3.2-1B is exceptionally fast, but it lacks the deep contextual understanding required for complex enterprise workflows. Qwen2.5-7B provides the ideal middle ground—it is lightweight enough to be deployed cost-effectively or run locally via Ollama, yet powerful enough to handle complex instructions reliably.
- Would your pick change for a multilingual or cost-sensitive use case, based on what you found in Part 3? Why or why not?
No, this choice becomes even more suitable for a multilingual or budget-conscious project due to Qwen's superior language optimization. Looking at the Part 3 tokenization test, Qwen’s vocabulary is clearly optimized for non-Latin scripts. It reduced the processing of the Chinese test sentence into just 5 tokens, while Llama 3.2 required 10 tokens. In a real-world application, cutting token usage in half directly translates to a 50% reduction in API operational costs or a 2x increase in processing speed during local inference. If a project involves heavy international localization, Qwen model is definitely more efficient, so I would stick with it.
- Would your pick change for a use case involving long documents (full reports, long transcripts), based on the context window math in Part 4? Why or why not?
My pick would still stay with Qwen2.5-7B. When looking at long-document use cases, the 128K context window across all three models means they can all mathematically fit Chapter 2's 45,467 tokens with plenty of room. Having a large context window is only useful if the model has the capacity to recall and reason over that data. Qwen's larger 7B parameter base guarantees much higher retrieval accuracy over long context spans compared to the compressed 1B architecture of Llama.

]

## Part 6: Graduate Extension — Paper / Technical Report Analysis (300–400 words)

*Graduate students required.*

Pick one of your 3 models that has a linked paper or technical report on its card (most do). Read enough of it to answer:

- One real detail from the paper that's not on the model card — training data composition, a specific benchmark, a stated limitation, whatever you find.
- At least one limitation or tradeoff the authors admit to themselves.
- Your own take: does reading the paper change how much you'd trust this model for a real project vs. just reading the card? Why or why not?

> [Write your analysis here]

## Grading (10 pts total)

| Component | Undergrad | Grad |
|---|---|---|
| Findings table (Part 2, incl. tokenizer field) | 3 pts | 3 pts |
| Tokenizer comparison exercise (Part 3) | 2 pts | 1 pt |
| Context window check (Part 4) | 2 pts | 1 pt |
| Comparison reflection (Part 5) | 3 pts | 2 pts |
| Graduate extension (Part 6) | — | 3 pts |
| **Total** | **10 pts** | **10 pts** |

*If a model's license, architecture, or vocab size isn't clearly labeled, say so in your reflection — not every card is well documented, and noticing that is a useful takeaway on its own.*
