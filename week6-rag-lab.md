# Week 6 Assignment — RAG Codelab + Your Own Documents



**Name:** Zhuo Ding
**Link to your completed Kaggle notebook:** https://www.kaggle.com/code/zhuoding/day-2-document-q-a-with-rag-c84589

---

## Overview

This week you'll work through a RAG lesson built by Google and Kaggle, then make it your own. Part 1 is completing their RAG question-answering codelab as written. In Part 2, you'll point that same pipeline at your own documents and test it with questions you write yourself. The reflection connects what you built back to Huyen's Chapter 6.

## Learning Objectives

- Build and run a working RAG pipeline: embed documents, store them, retrieve relevant passages, and generate grounded answers.
- Adapt an existing pipeline to a new set of documents.
- Evaluate retrieval separately from generation, so you can tell which part failed.
- Connect a hands-on implementation to the RAG architecture described in the textbook.

---

## Setup

1. Open the Kaggle Learn Guide linked above and go to **Day 2**.
2. Create a free Kaggle account if you don't have one. Kaggle may ask you to verify your account with a phone number before it allows internet access in notebooks, which the codelabs need.
3. Get a free Gemini API key from Google AI Studio.
4. Store your key using **Kaggle Secrets**, as the codelab instructs. **Never paste your key into a notebook cell.** Your notebook will be shared, and anyone who sees the key can use it.

If a cell fails, check the course's troubleshooting guide for the codelabs before spending a long time debugging.

---

## Part 1: Complete the RAG Codelab (30 pts)

Find the Day 2 codelab that builds a **RAG question-answering system over documents**. Copy it into your own Kaggle account and run it from top to bottom, with every cell executing successfully.

Record what the pipeline uses:

| | Value |
|---|---|
| Embedding model | `models/text-embedding-004` |
| Where the embeddings are stored (vector store/database) | `Chroma` (`ChromaDB`) |
| Generation model | `gemini-3.8-flash` |
| Number of passages retrieved per query | `1` |

**In 2–3 sentences, describe what happens between the moment a question is asked and the moment an answer comes back:**
After a question is submitted, the pipeline converts the text query into a vector representation using the `text-embedding-004` model. This embedding is passed to a localized `Chroma` vector store, which performs a similarity search to retrieve the single closest matching text passage (`n_results=1`). The retrieved text chunk is then combined with the user's original query inside a strict system prompt template and sent to `gemini-3.8-flash` to generate a grounded answer.

---

## Part 2: Make It Yours (40 pts)

In your copy of the notebook, **replace the sample documents with 3–5 short documents of your own.** Documents related to your term project are recommended. Course materials, public documentation for a tool you use, or articles on a topic you know well also work. Avoid anything private or sensitive.

Keep the rest of the pipeline the same. Your notebook should show your documents, your questions, and the outputs.

**Your documents:**

| | Value |
|---|---|
| What the documents are | Metadata data dictionaries, Washington State county mapping keys, and Data.WA.gov Socrata JSON API structural schemas. |
| Number of documents | 3 short instructional passages. |
| Why you chose them | These documents directly match my term project's metadata mapping requirements, allowing me to evaluate how well a RAG pipeline provides schema constraints to a downstream code-generation agent. |

Write **5 test questions** and run each through the pipeline. Your set must include:

- **2 keyword questions** that use exact names, terms, numbers, or codes from your documents
- **2 paraphrase questions** that ask about something in your documents without using its wording
- **1 unanswerable question** whose answer is **not** in your documents

| # | Question (short) | Type | Retrieved the right passage? (Yes / No / N/A) | Generated answer (correct / partly / wrong / correctly declined) |
|---|---|---|---|---|
| 1 | What is the exact column name for tracking Battery Electric Vehicles? | Keyword | Yes | correct |
| 2 | How does the schema label the primary key field for the Socrata API stream? | Keyword | No | wrong |
| 3 | What file handles the fallback dataset if the live state government network goes offline? | Paraphrase | Yes | correct |
| 4 | How should the pipeline clean up trailing spaces or lowercase county variants? | Paraphrase | No | wrong |
| 5 | Does this dataset track registration metrics for commercial aircraft flights? | Unanswerable | N/A | correctly declined |

**Pick one question where the result wasn't fully correct (or, if everything worked, the one that came closest to failing). Was the weak point retrieval or generation? How can you tell from the notebook's output?**
The weak point for Question 4 ("How should the pipeline clean up trailing spaces or lowercase county variants?") was **retrieval**. Looking at the notebook's output cells, the `Chroma` database failed to fetch the data dictionary passage containing string-cleaning rules, pulling instead an unrelated passage explaining API rate limits. Because the retrieval layer surface-matched peripheral terms and passed the wrong context chunk to `gemini-2.5-flash`, the generation model had no accurate reference data and produced an incorrect answer.

---

## Part 3: Reflection (30 pts, 250–350 words)

Answer all four:

- Huyen describes two families of retrievers: term-based and embedding-based. Which kind does the codelab use? Based on your keyword questions, where might the other kind have done better or worse?
- How did the pipeline handle your unanswerable question? What would happen in a real application if it handled that badly, and what would you change to fix it?
- The codelab was designed to work well on its own sample documents. What, if anything, got harder when you switched to yours?
- Your project evaluation plan is due next week with Milestone 1. Does your project need RAG? If so, what would the documents be, and if not, why not?

**Your reflection:**

The Kaggle lab uses an embedding retriever, which means it looks at the overall meaning of a sentence by using dense vectors. For my keyword questions, a traditional search method like BM25 probably would have been more reliable. When looking for an exact file name or a specific database column, keyword matching easily locks onto those exact characters. Embeddings can sometimes lose track of those unique strings if the surrounding text looks similar to another paragraph. However, for the paraphrase questions, BM25 would have totally failed. It cannot bridge the vocabulary gap when a user types a simple phrase like instead of matching the official documentation text.
When I gave the system the unanswerable question about aviation data, it handled it perfectly by refusing to answer. This works because the prompt explicitly tells Gemini to only use the retrieved text. If a real government data tool handled this badly and started making up fake stats, it would mislead transportation analysts. To fix this for a real production app, I would lower the similarity threshold in ChromaDB so it completely rejects weak matches, and I would change the system prompt to enforce a strict "Information not found" fallback answer.
Switching to my own documents showed that handling semantic ambiguity in user requests is much harder than dealing with raw data. Transport analysts will not use exact database column names; they might ask for "green cars around Seattle." The retrieval layer has to be strong enough to fetch mapping files that translate "green cars" into Battery Electric Vehicles and "around Seattle" into King County. If the RAG pipeline fetches the wrong layout rules, the agent will write perfectly functional Python code but generate a completely useless chart.
For next week's Milestone, my project definitely needs RAG. The system depends on database schemas and county keys that can change over time. Constantly fine-tuning a model on these small formatting updates would be a waste of money and compute power. A local RAG text dictionary is a much faster and more flexible way to give gpt-4o-mini the strict rules it needs to write working code.
---

