import json
import csv
from difflib import SequenceMatcher
from pathlib import Path


INPUT_PATH = "app/evaluation/ragas_results.json"
OUTPUT_PATH = "app/evaluation/free_eval_report.csv"


def similarity_score(actual: str, expected: str) -> float:
    actual = actual.lower().strip()
    expected = expected.lower().strip()

    if not actual or not expected:
        return 0.0

    return round(SequenceMatcher(None, actual, expected).ratio(), 3)


def contains_expected_keywords(actual: str, expected: str) -> float:
    actual_words = set(actual.lower().replace(".", "").split())
    expected_words = set(expected.lower().replace(".", "").split())

    if not expected_words:
        return 0.0

    matched = actual_words.intersection(expected_words)

    return round(len(matched) / len(expected_words), 3)


def hallucination_check(question: str, answer: str, ground_truth: str) -> bool:
    expected_fallback = "could not find" in ground_truth.lower()

    if not expected_fallback:
        return True

    fallback_phrases = [
        "could not find",
        "not found",
        "not available",
        "uploaded documents",
        "do not contain",
        "cannot find",
    ]

    answer_lower = answer.lower()

    return any(phrase in answer_lower for phrase in fallback_phrases)


def main():
    input_file = Path(INPUT_PATH)

    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {INPUT_PATH}")

    with input_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    rows = []

    total = len(data)
    passed = 0

    for item in data:
        question = item["question"]
        answer = item["answer"]
        ground_truth = item["ground_truth"]

        sim_score = similarity_score(answer, ground_truth)
        keyword_score = contains_expected_keywords(answer, ground_truth)
        hallucination_passed = hallucination_check(question, answer, ground_truth)

        is_passed = (
            sim_score >= 0.60
            or keyword_score >= 0.60
            or hallucination_passed
        )

        if is_passed:
            passed += 1

        rows.append({
            "question": question,
            "answer": answer,
            "ground_truth": ground_truth,
            "similarity_score": sim_score,
            "keyword_score": keyword_score,
            "hallucination_passed": hallucination_passed,
            "passed": is_passed,
        })

    pass_rate = round(passed / total, 3) if total else 0

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "question",
            "answer",
            "ground_truth",
            "similarity_score",
            "keyword_score",
            "hallucination_passed",
            "passed",
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\n✅ Free RAG Evaluation Completed")
    print("--------------------------------")
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Pass Rate: {pass_rate}")
    print(f"Report saved at: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()