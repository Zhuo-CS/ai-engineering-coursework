# Week 4 Evaluating and Comparing Two Models

## Part 1: Set Up Comparison （using arena.ai）

| | Model | Provider | Why you picked it |
|---|---|---|---|
| Model A | GPT-5.1 | OpenAI | Industry standard large size frontier model;perfect adherence to JSON formatting constrains, and robust multi-intent classification capability. |
| Model B | qwen3-vl-8b-instruct| Alibaba Group |Lightweigt, open-weight model; chose it to test whether a smaller, cost-effective model can handel structured JSON classification without breaking downstream parsing code. |

Write one prompt for the task and use it for both models

```
You are an AI assistant tailored for customer support operations.
Analyze the following customer support ticket and classify it into a single valid JSON object.

The output MUST strictly match this JSON schema:
{
  "category": "billing" | "technical" | "account_access" | "feature_request" | "other",
  "urgency": "low" | "medium" | "high",
  "needs_human": true | false
}

Rules:
1. "category" value must be exactly one of the 5 allowed strings.
2. "urgency" value must be exactly one of the 3 allowed strings.
3. "needs_human" must be a boolean (true or false). It should be true if the customer is angry, demanding money, experiencing severe breaking bugs, or requires manual account access verification.
4. Output ONLY the raw JSON object. Do not include markdown code blocks, backticks.

Ticket: [Insert 6 Ticket texts one by one here]
```

---

## Part 2: Define Your Criteria

Write three evaluation criteria for this task.

| # | Criterion | How you'd measure it | "Good enough" threshold |
|---|---|---|---|
| 1 | Format Cleanness | Check if the response contains only raw parseable JSON | All 6 tickets must be clean to avoid breaking code  |
| 2 | Functional Correctness| classification keys exist and the values matches | At least 5 out of 6 tickets are classified correct |   
| 3 | Lacency Performance |Measure the visual response time and streaming smoothness | continuous streaming and no long initial processing pauses |

---

## Part 3: Run Both Models

Here are six tickets with the correct answer for each. Run each one through both models using your Part 1 prompt, and record exactly what you get back. Copy it verbatim, including any extra words or formatting quirks. Those details matter for scoring. Do not give the model the refernece, that is meant for you.

| ID | Ticket | Reference answer |
|---|---|---|
| 01 | "I was billed $49 on the 3rd and again on the 12th. I only have one subscription. Please refund the duplicate." | `{"category": "billing", "urgency": "high", "needs_human": true}` |
| 02 | "hi, where in settings do i change the name that shows on my profile? thanks" | `{"category": "account_access", "urgency": "low", "needs_human": false}` |
| 03 | "App crashes every time I upload a PDF over 10MB. Been happening for three days." | `{"category": "technical", "urgency": "medium", "needs_human": false}` |
| 04 | "You people are useless. I've emailed four times about my refund and gotten nothing. I want my money NOW." | `{"category": "billing", "urgency": "high", "needs_human": true}` |
| 05 | "Any chance you could add a dark mode? The white background is rough at night." | `{"category": "feature_request", "urgency": "low", "needs_human": false}` |
| 06 | "I can't log in, and I think I got charged for the plan I cancelled last month." (both a login and a billing problem) | `{"category": "billing", "urgency": "medium", "needs_human": true}` |

Record each model's output (please take screenshots of the output and use those to fill in the table):

| ID | Model A output (verbatim) | Model B output (verbatim) |
|---|---|---|
| 01 |{"category": "billing", "urgency": "high", "needs_human": true}  | {"category": "billing", "urgency": "medium", "needs_human": true} |
| 02 | {"category": "technical", "urgency": "low", "needs_human": false} | {"category": "feature_request", "urgency": "low", "needs_human": false} |
| 03 | {"category": "technical", "urgency": "high", "needs_human": true} | {"category": "technical", "urgency": "high", "needs_human": false} |
| 04 | {"category": "billing", "urgency": "high", "needs_human": true} | {"category": "billing", "urgency": "high", "needs_human": true} |
| 05 | {"category": "feature_request", "urgency": "low", "needs_human": false} | {"category": "feature_request", "urgency": "low", "needs_human": false} |
| 06 | {"category": "billing", "urgency": "high", "needs_human": true} | {"category": "account_access", "urgency": "high", "needs_human": true} |

Note which model felt slower to respond. Model B
---

## Part 4: Score What You Got

Score the outputs two ways. Here's what each one means:

**Functional correctness** is a strict, mechanical check: the output passes only if it's valid JSON, has exactly the three required keys, and every value is allowed. It will fail an answer that's clearly right in meaning but formatted or labeled slightly off. Watch for that as you go.

**Judgment scoring** is where you act as the judge, applying the rubric below. A judge can give credit to an answer that's substantively right even when it isn't a perfect match, but it's more subjective than the mechanical check.

Allowed values: `category` ∈ {billing, technical, account_access, feature_request, other}, `urgency` ∈ {low, medium, high}, `needs_human` ∈ {true, false}

### 4a. Functional-correctness check

Mark each output pass or fail. Where it fails, say why.

| ID | A: pass/fail | A — reason if fail | B: pass/fail | B — reason if fail |
|---|---|---|---|---|
| 01 | pass | NA | pass | NA |
| 02 | pass | NA | pass | NA |
| 03 | pass | NA | fail | NA |
| 04 | pass | NA | pass | NA |
| 05 | pass | NA | pass | NA | 
| 06 | pass | NA | fail | NA |

Functional-correctness score — Model A: _6__ / 6   Model B: _6__ / 6

### 4b. Judgment scoring

Score each output 1–5:

> **5** — Correct classification, clean and usable output.
> **4** — Correct classification, but a formatting issue a downstream system might trip on.
> **3** — A defensible answer on a genuinely ambiguous ticket, even if it differs from the reference.
> **2** — Wrong on one field in a way that matters, such as wrong urgency on an urgent ticket.
> **1** — Wrong category, or unusable output.

| ID | A: judge score | B: judge score |
|---|---|---|
| 01 | ___5__ | __4___ |
| 02 | __1__ | __1___ |
| 03 | ___2__ | ___2__ |
| 04 | __5___ | __5__ |
| 05 | __5___ | __5_ |
| 06 | ___5__ | __2_ |


> Ticket 06 on Model B is a perfect example of where the two grading methods completely disagreed. Model B generated a totally clean JSON object with no syntax errors, so it passed the strict functional check. But it misclassified a major billing dispute as a regular account access issue, which means the ticket would have been sent to the wrong department and ignored. Because of that, I gave it a judgment score of 2.
For this ticket, the human judgment method was way closer to the truth. A strict code check only tells you if the formatting is clean enough to keep your app from crashing, but it has no clue if the actual data inside makes sense. A model can pass all formatting tests while passing completely wrong answers down the line. So we can't just rely on automated syntax checks alone; we need an actual review to make sure the AI's logic is right.

---

## Part 5: Recommendation and Reflection (200–300 words)

Evaluation and Selection:
Model A (GPT-5.1) is definitely the better model to go with here. It crushed both parts of the grading, getting a perfect 6/6 functional score and a 23/30 on judgment. What really stood out was how it handled Ticket 06. While Qwen got distracted by the login issue and threw it into account access, GPT-5.1 correctly flagged that a user complaining about getting wrongfully charged after canceling needs to go straight to a human billing agent.
Tradeoffs:
The main catch with picking a massive commercial model like GPT-5.1 is that you miss out on the cost efficiency and data privacy of open-weight models like Qwen. Running an 8B model on your own hardware or a cheap cloud instance is basically free at scale and keeps all user data fully in-house. With GPT-5.1, you are paying ongoing API costs and sending sensitive customer support data to a third-party vendor.
Scaling Challenges and Automation Pipelines:
Grading 12 outputs by hand wasn't too bad, but doing this for 200 tickets would be incredibly time-consuming and lead to a lot more human errors. To make the process more efficient and avoid those mistakes, I would set up an automated evaluation pipeline. The script would instantly check if the output is valid JSON, and then use GPT-5.1 as an "LLM-as-a-Judge" to compare the answers against our ground-truth labels. This turns tedious manual clicking into a code script that runs in seconds.
Dataset Constraints:
Making a final production decision based on just six tickets is simply not enough. A tiny dataset like this doesn't include any of the messiness of real support queues, like typos, weird formatting, extra spaces, or non-English messages. Smaller models can look surprisingly good on a few clean examples, but they often fall apart once you hit them with unpredictable real-world scenarios.
---

