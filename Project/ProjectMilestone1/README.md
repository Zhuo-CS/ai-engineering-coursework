# Autonomous Public Sector Data Analysis Agent

An autonomous data manipulation and validation engine designed to standardize Washington State Electric Vehicle registries, construct dynamic chart visualization workflows, and intercept adversarial string execution hazards.

## How to Install and Run

### 1. Installation Requirements
Ensure you have Python 3 deployed. Install the required client software packages via pip:
```bash
pip install openai
```

### 2. Configure System Variables
This repository does not employ `.env` files to maintain strict credential safety. Ensure your host environment variable is mounted directly into your host terminal session:
```powershell
# For Windows PowerShell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-key-here", "User")
```

### 3. Running the Single-Command Evaluation Pipeline
Run the fully automated evaluation test-bench against any cloud-based or local backend dynamically using command-line arguments without modifying code:

```bash
# 1. Evaluate Commercial Cloud Hub
python evaluate.py --model gpt-4o-mini

# 2. Evaluate Local Open-Weight Models (Ensure Ollama is running in background)
python evaluate.py --model qwen2.5:3b
python evaluate.py --model llama3.2:3b
```
