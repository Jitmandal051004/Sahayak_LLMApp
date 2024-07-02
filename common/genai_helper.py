import os
from llm_app.model_wrappers import LiteLLMChatModel, LiteLLMEmbeddingModel
import pathway as pw

embedder_locator = os.environ.get("EMBEDDER_LOCATOR", "huggingface/microsoft/codebert-base")
os.environ["HUGGINGFACE_API_KEY"] = "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"
model_locator = os.environ.get("MODEL_LOCATOR", "huggingface/codellama/CodeLlama-34b-Instruct-hf")
max_tokens = int(os.environ.get("MAX_TOKENS", 1000))
temperature = float(os.environ.get("TEMPERATURE", 0.0))

def genai_embedder(data):
    embedder = LiteLLMEmbeddingModel()
    return embedder.apply(text=data, locator=embedder_locator)


def genai_chat_completion(prompt):
    print(prompt)
    model = LiteLLMChatModel()

    return model.apply(
            prompt,
            locator=model_locator,
            temperature=temperature,
            max_tokens=max_tokens,
        )

