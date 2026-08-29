# AI Engineering Coursework

This repository contains the assignments completed for the AI Engineering course.

## Project Structure
- `api_call.py`: Python script to interact with a hosted LLM provider Openai via API.
- `output_api.txt` (or screenshot): Evidence of the successful hosted API call output.
- `output_ollama.txt` (or screenshot): Evidence of the local Ollama model execution.
- `README.md`: Project overview and setup instructions.

---

## Part A: Hosted API Call

### Setup Environment Variable (Windows)
Before running the script, set API key as an environment variable in Windows PowerShell:

```powershell
setx OPENAI_API_KEY "your_actual_api_key_here"
```
*Note: Restart your terminal after running this command to apply the changes.*

### Installation
Install the required OpenAI SDK:
```powershell
pip install openai
```

### Running the Script
Run the hosted API script using:
```powershell
py api_call.py
```

---

## Part B: Local Model Attempt (Ollama)

### Setup & Run
1. Downloaded and installed Ollama for Windows from ollama.com
2. Opened the terminal and executed the following commands to pull and run the local model:
   ```powershell
   ollama pull llama3.2:3b
   ollama run llama3.2:3b
   ```
3. Verified the setup by conducting a successful back-and-forth chat session directly inside the Windows terminal.

*Note: See the repository files (`output_ollama.txt` or screenshot) for evidence of the successful terminal chat session.*

