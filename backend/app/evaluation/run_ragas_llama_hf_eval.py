import json
import os

from dotenv import load_dotenv
from datasets import Dataset

from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_huggingface import HuggingFaceEmbeddings

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
    """
    Loads Postman-collected RAG outputs for RAGAS evaluation.

    Expected JSON format:

    [
      {
        "question": "What is the policy renewal period?",
        "answer": "The policy renews every 12 months.",
        "contexts": [
          "The customer protection policy renews every 12 months."
        ],
        "ground_truth": "The policy renews every 12 months."
      }
    ]
    """

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    rows = []

    for item in data:
        rows.append(
            {
                # Your ragas version may output these as user_input/retrieved_contexts/response/reference
                # but passing question/contexts/answer/ground_truth is accepted by many ragas versions.
                "question": item["question"],
                "answer": item["answer"],
                "contexts": item["contexts"],
                "ground_truth": item["ground_truth"],
            }
        )

    return Dataset.from_list(rows)


def main():
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        raise ValueError(
            "HF_TOKEN is missing. Add HF_TOKEN=your_token_here to your .env file."
        )

    dataset = load_ragas_results()

    # LLM judge through Hugging Face Inference API / Inference Providers.
    # This does NOT download Llama locally.
    base_llm=HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct",
        task="text-generation",
        huggingfacehub_api_token=hf_token,
        temperature=0.0,
        max_new_tokens=512,
        do_sample=False,
        timeout=120,
        provider="auto",
    )
    chat_llm = ChatHuggingFace(llm=base_llm)
    evaluator_llm = LangchainLLMWrapper(chat_llm)

    # Small embedding model. This runs locally, but it is lightweight compared to an LLM.
    # Needed for answer_relevancy.
    evaluator_embeddings = LangchainEmbeddingsWrapper(
        HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            },
        )
    )

    run_config = RunConfig(
        timeout=120,
        max_retries=2,
        max_workers=1,
    )

    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,        # generation quality: answer supported by context
            answer_relevancy,    # generation quality: answer matches question
            context_precision,   # retrieval quality: retrieved chunks are useful
            context_recall,      # retrieval quality: retrieved chunks contain enough answer info
        ],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
        run_config=run_config,
    )

    print("\n✅ RAGAS + Llama 3.1 8B Instruct Evaluation Result")
    print(result)

    df = result.to_pandas()

    output_path = "app/evaluation/ragas_llama_hf_report.csv"
    df.to_csv(output_path, index=False)

    print(f"\n✅ Report saved at: {output_path}")


if __name__ == "__main__":
    main()