from letta import LLMConfig, EmbeddingConfig

EMBEDDING_CONFIG = EmbeddingConfig(
    embedding_endpoint_type="hugging-face",
    embedding_endpoint="https://embeddings.memgpt.ai",
    embedding_model="letta-free",
    embedding_dim=1024,
    embedding_chunk_size=300,
)

LLM_CONFIG = LLMConfig(
    model="letta-free",
    model_endpoint_type="openai",
    model_endpoint="https://inference.memgpt.ai",
    model_wrapper=None,
    context_window=16384,
)
