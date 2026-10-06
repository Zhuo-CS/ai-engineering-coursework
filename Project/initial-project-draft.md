# Project Draft: Autonomous Public Sector Data Analysis Agent

## Section 1: Problem Statement

The goal of this system is to take a live dataset tracking the registered Electric Vehicle (EV) population across different Washington State counties, clean up layout and text inconsistencies via automated Python scripts, and produce accurate visualization charts based on what a user asks for in English such as "Plot the growth trend of battery electric vehicles in King County for the last quarter".

Right now, transportation analysts and program coordinators in regional planning offices have to dig through massive vehicle registries manually, which is a slow and clunky process. Whenever leadership asks for an update on green infrastructure or charging station allocation, staff have to log into public portals, export giant tabular files, and manually sort through thousands of rows in Excel to filter out specific vehicle categories or counties. This manual copy-pasting takes up way too much time and easily leads to accidental human errors.

This is an AI engineering problem rather than something a basic programming script or standard search box can fix. Government database records contain discrepancies and unexpected formatting text anomalies. For instance, one data entry row might log a region as "King County", while another enters it as "King county " or leaves extra white spaces that standard scripts can't read. A traditional script is completely rigid—it looks for exact matches and crashes or drops data the second it runs into these formatting variations. We need an LLM's reasoning capabilities to understand these naming quirks on the fly, use a local data dictionary to standardize inputs, and automatically write the Python code to filter the dataset and render the charts.

## Section 2: Target Users
The main users for this tool will be junior data analysts, administrative assistants, and program managers working inside regional transport or economic development branches. They will interact with this system through a simple, chat-based webpage workspace whenever they need to pull a localized vehicle trend quickly or generate an executive visualization slide for an unexpected management meeting.

Success for them means:
* **High Trust:** The system correctly interprets typo variations or clipped county names and grabs the exact vehicle metrics they asked for.
* **Speed:** Users receive a complete, functional chart and a brief text explanation in seconds just by typing a single conversational sentence.

Users will stop using the tool if:
* The generated Python code constantly throws syntax errors or crashes the local host application.
* The system suffers from semantic hallucinations or misaligning time blocks, creating completely misleading or inaccurate data plots.

## Section 3: Candidate Approach

This project will use a **simplified agent pipeline combined with a basic local Retrieval-Augmented Generation (RAG) metadata setup**. An independent agent control loop is needed because the system has to process tasks sequentially on its own: read the user's plain text request, inspect the live data schemas, select the right pandas tool, write the execution code, double-check that the code is completely safe, run it locally, and handle any unexpected syntax errors if they pop up.

My architectural framework combines a cloud model and a local open model to keep things running efficiently without costing too much:
* **Hosted Core Engine (OpenAI gpt-4o-mini):** This serves as my primary reasoning and code-generation hub. It is selected due to its exceptional accuracy in writing clean Python code and manipulating dataframes at an low API token cost.
* **Local Metadata RAG (Ollama / Local Text Files):** Instead of dealing with an over-complicated cloud vector database, I will use a lightweight local data dictionary text file powered by Ollama to store my target dataset's file structure along with a county mapping guide. This gives `gpt-4o-mini` clear operational boundaries so it doesn't write broken filtering code.
* **Local Security Guardrail (Ollama / Llama 3.2:3b):** Running AI-generated string code on a local machine using Python's `exec()` function is a security risk. To protect the host computer, I will use a local Llama 3.2 instance as an active security gatekeeper. Before the generated script actually runs, Llama 3.2 will scan the code text string and completely block any dangerous OS-level commands (ex. deleting files or altering system directories).

**Alternative Considered (Finetuning):** Public reporting formats and dataset schemas change over time. Finetuning is expensive, takes a lot of computing power, gets outdated quickly, and can't adapt to real-time schema changes. Using a local RAG text dictionary with precision prompting is a much faster and more flexible solution for this scale.

The hardest part of the project will definitely be **safe code execution**. Since running dynamic strings through `exec()` is inherently risky, making sure the guardrail model successfully catches bad or malicious code blocks is the most critical part of my system architecture.

## Section 4: Evaluation Plan

I will test how well this prototype works by building an automated evaluation script (`evaluate.py`) that scores three concrete metrics:

1. **Code Execution Success Rate:** I will create a test set of 20 realistic user prompts asking for various Washington counties, specific vehicle models, and different chart types. I will measure the percentage of times the agent's code runs perfectly without throwing a single Python error. My success target is **>= 85%**.
2. **Naming Standardization Accuracy:** I will intentionally include typos, lowercase names, or short abbreviations in my test prompts (like "King county " or "pierce"). I will track how often the agent successfully fixes these inputs to match the actual dataset columns using my local RAG rules. My target is **100% accuracy**.
3. **Guardrail Safety Interception Rate:** I will mix 10 adversarial prompts containing hidden malicious commands (for example, trying to overwrite local system files) into my test bench. My target is a strict **100% block rate** by my local Llama 3.2 check.

**Baseline for Comparison:** My baseline will be a "naive" version of the app where user queries go straight to GPT-4o-mini without any local RAG metadata or cleaning instructions. I will compare the code success rate of my full system against this baseline to quantitatively prove that my RAG data dictionary actually makes a difference in preventing code failures.

My testing data will be built using live streams from the official Data.WA.gov Socrata JSON API via the official registry [Electric Vehicle Population Data](https://wa.gov), backed up by a downloaded local CSV snapshot (**`electric_vehicle_snapshot.csv`**) inside my repository workspace.

To handle realistic failure cases on purpose, I will use a **"Live-First with Local Fallback" pattern**. The agent will try to fetch live data directly from the web API first. If the network drops or the government site is down, the script will catch the error, pop up a warning alert on the screen, and seamlessly load my local fallback CSV snapshot so the user can still get their chart without system downtime.

The harder thing to measure quantitatively will be the aesthetic quality of the graphs, which I will just have to review manually by looking at them.
