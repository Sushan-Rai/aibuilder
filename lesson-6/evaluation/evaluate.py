import os
import sys
import json
import time

# Ensure app directories are in python path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "app"))

from app.agent import run_agent

dataset = json.load(
    open("evaluation/dataset.json")
)

results = []

for item in dataset:
    start = time.time()
    try:
        answer = run_agent(
            item["input"]
        )
        success = True
    except Exception as e:
        answer = str(e)
        success = False

    latency = time.time() - start

    results.append(
        {
            "question": item["input"],
            "expected": item["expected"],
            "answer": answer,
            "latency_seconds": round(latency, 3),
            "tool_success": success
        }
    )

json.dump(
    results,
    open(
        "evaluation/results.json",
        "w"
    ),
    indent=4
)

print("Evaluation complete")
