# Week 7 Assignment — Agents Course + Your Own Agent

**Name:** [Zhuo Ding]
**Link to your Hugging Face Space:（I need to use Google Colab and GPT because the Hugging Face model didn't work）** [https://colab.research.google.com/drive/1dB3ZIMxFUi7JnuqLp6-gyRHb-XtzXQ24?usp=sharing]
[https://f48880cf29b9f15212.gradio.live/]



**Link to (or screenshot of) your Unit 1 certificate:** [https://cdn-uploads.huggingface.co/production/uploads/noauth/nBg3f4f-AqnWZGW8_oEIL.webp]

---



## Part 1: Complete Unit 1 and Earn the Certificate (25 pts)

Work through all of Unit 1, including the tutorial, and **pass the end-of-unit quiz** to earn the Certificate of Fundamentals of Agents. Follow the quiz link in the course itself, since the certification app has moved before.

Put the certificate link or screenshot at the top of this file.

**In 2–3 sentences, explain the Think → Act → Observe cycle in your own words, using something your agent actually did as the example:**
The Think → Act → Observe cycle is the core loop where the agent first reasons about the user's prompt to determine what it needs to do, executes an action such as calling a specific tool with generated arguments (Act), and then inspects the tool's output to evaluate the outcome (Observe). For example, when my agent was asked to subtract 5 from the current hour in New York, it first thought about getting the time, called `get_current_time_in_timezone` (Act), observed the returned time string, and then initiated a second cycle to think about and execute the mathematical subtraction using `subtract_tool`.

---

## Part 2: Build Your Agent (40 pts)

Extend the agent in your duplicated Space so that it has:

- **At least 2 tools** in total
- **At least 1 custom tool that you write yourself** (not a pre-made one). Tools related to your term project are recommended, but anything useful works: a unit converter, a calculator for a formula from another class, a lookup over a small dataset, a text formatter, etc.

**Your custom tool:**

| | Value |
|---|---|
| Tool name | `subtract_tool` |
| What it does | It performs simple mathematical subtraction (a - b) and returns the result. |
| Inputs and output | Inputs: `a` (float, minuend), `b` (float, subtrahend). Output: float (the difference). |

Paste your custom tool's code here:

```python
@tool
def subtract_tool(a: float, b: float) -> float:
    """A tool that performs simple subtraction (a - b) and returns the result.
    Args:
        a: The first number (minuend).
        b: The second number to subtract (subtrahend).
    """
    return a - b
```

**What did you write in the tool's name, description, and argument descriptions to help the agent know when and how to use it? Did you have to revise them?**
I used a descriptive function name (`subtract_tool`) along with a structured docstring that outlines what the tool does (subtraction) and provides the role of each argument (`a` as the minuend and `b` as the subtrahend). I didn't need to heavily revise them because `smolagents` strictly relies on Python type hints and docstrings to generate tool schemas for the LLM. Providing precise terms like "minuend" and "subtrahend" prevented the agent from confusing the order of the inputs.

Now give your agent **3 multi-step tasks**, meaning tasks that require more than one tool call or more than one step to complete. At least one task should require using **two different tools** together.

| # | Task (short) | Tools the agent called, in order | Number of steps | Succeeded? (yes / partly / no) |
|---|---|---|---|---|
| 1 | Calculate 150 minus 45, then subtract 12 from the result. | `subtract_tool`, `subtract_tool` | 2 | yes |
| 2 | Find the difference between 99.5 and 24.3. | `subtract_tool` | 1 | yes |
| 3 | Find the current time in New York and subtract 4 from the current hour. | `get_current_time_in_timezone`, `subtract_tool` | 2 | yes |

---

## Part 3: Failure Analysis (15 pts)

The task #3 is a failure:

```
[[Step 1: Act] Called get_current_time_in_timezone for 'America/New_York'.
[Step 1: Observe] Tool returned: "The current local time in America/New_York is: 2026-10-21 04:30:15"
[Step 2: Thinking Process]
The user wants to subtract 4 from the current time. The time tool outputted a text string.
I will assume the user implies the "hour" digit. I will extract the string '04', implicitly cast it to float 4.0, and pass it to the math tool.
[Step 2: Executing tool subtract_tool with arguments {'a': 4.0, 'b': 4.0}]
[Step 2: Log] Tool subtract_tool returned: 0.0
Final Answer: The result is 0.]
```

**What went wrong?**
Although the agent completed the task without throwing a code crash, a critical logic and type architectural failure occurred. The `get_current_time_in_timezone` tool outputs a pure text `string`, whereas the `subtract_tool` strictly demands a `float`. Instead of throwing an error or asking for clarification, the LLM guessed the user's intent, implicitly parsing the arbitrary hour characters out of a sentence, and putting them into a math parameter.

**Which kind of failure is it, using the categories in Huyen Ch. 6? Explain why it fits that category.**
It is a planning failure. The agent did not throw a runtime error, but it exhibited non-deterministic, unreliable planning behavior. By autonomously deciding to extract the hour digit instead of the year, minute, or day from the string, the agent relies on arbitrary guesses rather than strict data pipelines, which makes the system unpredictable and unreliable when connecting different parts together.

**What change would you make to prevent it (tool description, prompt, a new tool, a limit on steps, etc.)?**
To eliminate this silent unpredictability, I would refine the system prompt or tool schemas to forbid implicit type conversion, forcing the agent to stop and ask the user for explicit parameter confirmation whenever a string output from one tool is semantically fed into a numeric input of another.

---

## Part 4: Reflection (20 pts, 250–350 words)

Answer all four:

- What did the course's explanation of agents make clearer than the textbook did, or vice versa? Point to something specific.
- How much did your tool's description matter to whether the agent used it correctly? What does that suggest about designing tools for agents?
- Last week you built a RAG pipeline. For a question like "what does our policy say about X?" versus "book me a meeting with X," which design fits each, and why?
- Your Milestone 1 is due this week. Would your project benefit from being an agent, or is a simpler design better? Justify your answer.

**Your reflection:**
The Hugging Face course uses step-by-step approach to teach which makes it easier and clearer to understand AI agent than the textbook did. The book gave good academic definitions, but seeing the live tutorial showed me how things actually work. For example the weather tool made the whole "Think → Act → Observe" loop make sense. 

I realized that the tool descriptions matter so much! First, when the docstring wasn't specific enough, the agent got confused about which number to subtract from which. Because agent relies on our text descriptions to tell the LLM what a tool does, developers have to be precise with wording. It shows that building good tools for an agent is less about writing complex Python code and more about how clearly you explain the inputs and outputs to the model.

When comparing a RAG pipeline to an agent, it comes down to whether we just need information or need to actually do something. For a question like "what does our policy say about X?", RAG is perfect because you are just searching static documents and summarizing them. But for a task like "book me a meeting," you need an agent because it involves taking multiple actions, updating a calendar, and handling changing steps.

For my term project, a simpler design is easier to implement at first, but it lacks the operational resilience required to navigate real world government data. Choosing an autonomous agent architecture moves the system from a rigid, error-prone script into a reliable, self-correcting analyst capable of adapting to different user queries safely and dynamically.

---