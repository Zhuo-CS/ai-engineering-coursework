import json
import time
import argparse
from main import answer

def run_evaluation(model_name: str):
    with open("eval_set.json", "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    print(f"\n=======================================================")
    print(f"LAUNCHING AUTOMATED EVALUATION SET FOR: {model_name}")
    print(f"=======================================================")

    total_cases = len(eval_set)
    passed_cases = 0
    total_latency = 0.0

    for idx, case in enumerate(eval_set):
        question = case["question"]
        expected_keywords = case["expected_keywords"]

        # Track isolated model turnaround timing
        start_time = time.time()
        output = answer(question, model_name=model_name)
        elapsed_time = time.time() - start_time
        
        total_latency += elapsed_time

        # Verification: Validate alignment with evaluation criteria assertions
        passed_check = any(kw.lower() in output.lower() for kw in expected_keywords)
        
        if passed_check:
            passed_cases += 1
            status = "PASS"
        else:
            status = "FAIL"

        print(f"[{idx+1:02d}/{total_cases:02d}] Type: {case['type']:<18} | Time: {elapsed_time:.2f}s | Result: {status}")
        
        if status == "FAIL":
            print(f"   -> Prompt: {question}")
            print(f"   -> Agent Output: {output}\n")

    # Metrics aggregation
    accuracy_score = (passed_cases / total_cases) * 100
    average_latency = total_latency / total_cases

    print(f"\n================ SUMMARY REPORT ================")
    print(f"Target Evaluation Model  : {model_name}")
    print(f"Functional Pass Score    : {accuracy_score:.1f}% ({passed_cases}/{total_cases})")
    print(f"Average Response Latency : {average_latency:.2f} seconds")
    print(f"================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Target evaluation model selection.")
    args = parser.parse_args()

    run_evaluation(args.model)
