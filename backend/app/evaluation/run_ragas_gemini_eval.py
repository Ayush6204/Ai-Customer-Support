import json
import os

from dotenv import load_dotenv
from datasets import Dataset

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig


load_dotenv()


def load_ragas_results(path: str = "app/evaluation/ragas_results.json") -> Dataset:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    rows = []

    for item in data:
        rows.append(
            {
                "question": item["question"],
                "answer": item["answer"],
                "contexts": item["contexts"],
                "ground_truth": item["ground_truth"],
            }
        )

    return Dataset.from_list(rows)


def main():
    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY is missing. Add it to your .env file.")

    dataset = load_ragas_results()

    evaluator_llm = LangchainLLMWrapper(
        ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=google_api_key,
            timeout=120,
            max_retries=2,
        )
    )

    evaluator_embeddings = LangchainEmbeddingsWrapper(
        GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=google_api_key,
        )
    )

    run_config = RunConfig(
        timeout=120,
        max_retries=5,
        max_workers=1,
    )

    result = evaluate(
        dataset=dataset,
        metrics=[
            # faithfulness, #generation
            # answer_relevancy, #generation
            # context_precision, #retrieval
            # context_recall, #retrieval
        ],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
        run_config=run_config,
    )

    print("\n✅ RAGAS + Gemini Evaluation Result")
    print(result)

    df = result.to_pandas()

    output_path = "app/evaluation/ragas_gemini_report.csv"
    df.to_csv(output_path, index=False)

    print(f"\n✅ Report saved at: {output_path}")


if __name__ == "__main__":
    main()