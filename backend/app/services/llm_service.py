from fastapi import HTTPException, status
from google import genai
from google.genai import types
from huggingface_hub import InferenceClient

from app.core.config import settings


# ------------------------------------------------------------------
# Gemini Client & Generator
# ------------------------------------------------------------------
def get_gemini_client() -> genai.Client:
    if not settings.GOOGLE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GOOGLE_API_KEY is missing. Add it in your .env file."
        )

    return genai.Client(api_key=settings.GOOGLE_API_KEY)


def generate_answer_with_gemini(prompt: str) -> str:
    print("LLM service (generate answer with Gemini) -->")

    try:
        client = get_gemini_client()

        # Configure response constraints using config settings
        config = types.GenerateContentConfig(
            temperature=settings.LLM_TEMPERATURE,
            max_output_tokens=settings.LLM_MAX_TOKENS,
            system_instruction=(
                "You are a helpful RAG assistant. "
                "Answer only from the provided uploaded document context. "
                "If the answer is not in the context, say: "
                "'I cannot find this information in your uploaded documents.'"
            ),
        )

        response = client.models.generate_content(
            model=settings.GEMINI_LLM_MODEL,
            contents=prompt,
            config=config,
        )

        answer = response.text

        if not answer or not answer.strip():
            return "I could not generate an answer right now."

        return answer.strip()

    except Exception as e:
        error_text = str(e)
        return f"Gemini LLM generation failed: {error_text}"


# ------------------------------------------------------------------
# Hugging Face Client & Generator
# ------------------------------------------------------------------
def get_huggingface_client() -> InferenceClient:
    if not settings.HF_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="HF_TOKEN is missing. Add it in your .env file."
        )

    return InferenceClient(
        provider=settings.HF_INFERENCE_PROVIDER,
        api_key=settings.HF_TOKEN,
    )


def generate_answer_with_huggingface(prompt: str) -> str:
    print("LLM service (generate answer with Hugging Face) -->")

    try:
        client = get_huggingface_client()

        completion = client.chat.completions.create(
            model=settings.HF_LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful RAG assistant. "
                        "Answer only from the provided uploaded document context. "
                        "If the answer is not in the context, say: "
                        "'I cannot find this information in your uploaded documents.'"
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=settings.LLM_MAX_TOKENS,
            temperature=settings.LLM_TEMPERATURE,
        )

        answer = completion.choices[0].message.content

        if not answer or not answer.strip():
            return "I could not generate an answer right now."

        return answer.strip()

    except Exception as e:
        error_text = str(e)

        if "402" in error_text or "Payment Required" in error_text:
            return (
                "The relevant document content was found, but Hugging Face provider billing/credits "
                "are required for this model/provider."
            )

        if "401" in error_text or "Unauthorized" in error_text:
            return (
                "The relevant document content was found, but Hugging Face authentication failed. "
                "Please check your HF_TOKEN."
            )

        if "403" in error_text or "gated" in error_text.lower():
            return (
                "The relevant document content was found, but access to this Llama model is blocked. "
                "Please accept the model license on Hugging Face and check your token permissions."
            )

        if "429" in error_text or "rate" in error_text.lower():
            return (
                "The relevant document content was found, but Hugging Face rate limit was reached. "
                "Please try again later."
            )

        return f"Hugging Face LLM generation failed: {error_text}"


# ------------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------------
def generate_answer_from_prompt(prompt: str) -> str:
    print("LLM service (generate answer from prompt) -->")

    provider = settings.LLM_PROVIDER.lower().strip()

    if provider == "gemini":
        return generate_answer_with_gemini(prompt)

    if provider == "huggingface":
        return generate_answer_with_huggingface(prompt)

    return "No valid LLM provider configured."