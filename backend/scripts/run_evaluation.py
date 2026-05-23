import sys
import os
from collections import defaultdict

# Add backend to path so we can import analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analyzer.core import Analyzer
from tests.eval_data import EVALUATION_DATASET

def run_evaluation():
    analyzer = Analyzer()
    
    total_cases = len(EVALUATION_DATASET)
    passed_cases = 0
    failed_cases = 0
    
    total_missed = 0
    total_unexpected = 0
    
    rule_results = defaultdict(lambda: {"triggered": 0, "missed": 0, "false_positive": 0})
    
    print("========================================")
    print(" PyMentor Review - Evaluation Runner")
    print("========================================\n")
    
    for case in EVALUATION_DATASET:
        report = analyzer.analyze(case["code"])
        found_ids = {f.id for f in report.findings}
        
        expected = set(case["expected_present"])
        absent = set(case["expected_absent"])
        
        missed = expected - found_ids
        unexpected = found_ids.intersection(absent)
        
        # We also want to track any findings that were totally unexpected (not in expected_present and not explicitly tested in absent, but found). 
        # But for evaluation, we only care about violations of 'expected_present' and 'expected_absent'.
        
        if not missed and not unexpected:
            passed_cases += 1
            status = "✅ PASS"
        else:
            failed_cases += 1
            status = "❌ FAIL"
            total_missed += len(missed)
            total_unexpected += len(unexpected)
            
        print(f"[{case['category']}] {case['name']} - {status}")
        
        if missed:
            print(f"   -> Missed expected: {missed}")
            for m in missed:
                rule_results[m]["missed"] += 1
                
        if unexpected:
            print(f"   -> Unexpectedly found: {unexpected}")
            for u in unexpected:
                rule_results[u]["false_positive"] += 1
                
        # Track successfully triggered rules
        for f in expected.intersection(found_ids):
            rule_results[f]["triggered"] += 1
            
    print("\n========================================")
    print(" Evaluation Summary")
    print("========================================")
    print(f"Total Cases:       {total_cases}")
    print(f"Passed Cases:      {passed_cases}")
    print(f"Failed Cases:      {failed_cases}")
    print(f"Total Missed:      {total_missed}")
    print(f"Total Unexpected:  {total_unexpected}")
    
    print("\nPer-Rule Results:")
    print(f"{'Rule ID':<25} | {'Triggered':<10} | {'Missed':<10} | {'False Positive':<15}")
    print("-" * 65)
    for rule_id, stats in sorted(rule_results.items()):
        print(f"{rule_id:<25} | {stats['triggered']:<10} | {stats['missed']:<10} | {stats['false_positive']:<15}")
        
    print("\n")
    if failed_cases > 0:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    run_evaluation()
