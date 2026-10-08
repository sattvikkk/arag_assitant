import os

import logfire
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()

BATCH_SIZE = 50
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-small-en-v1.5",
)

_active_model = None
_embedding_dim = None


def _init() -> None:
    """Initialize the local embedding model once."""
    global _active_model, _embedding_dim

    if _active_model is not None:
        return

    with logfire.span(
        "Initialize embedding model",
        model=EMBEDDING_MODEL,
    ):
        _active_model = SentenceTransformer(EMBEDDING_MODEL)

        _embedding_dim = (
            _active_model.get_sentence_embedding_dimension()
        )

        logfire.info(
            f"Embedding model ready: "
            f"{EMBEDDING_MODEL} ({_embedding_dim}-dim)."
        )


def get_embedding_dim() -> int:
    """Return embedding dimension for Qdrant."""
    _init()
    return _embedding_dim


def embed_query(query: str) -> list[float]:
    """Embed a single query."""
    _init()

    embedding = _active_model.encode(
        query,
        normalize_embeddings=True,
    )

    return embedding.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed document chunks in batches."""
    _init()

    clean_texts = [
        text for text in texts
        if text and text.strip()
    ]

    all_embeddings = []

    for i in range(0, len(clean_texts), BATCH_SIZE):
        batch = clean_texts[i:i + BATCH_SIZE]

        with logfire.span(
            "Embed batch",
            model=EMBEDDING_MODEL,
            start=i,
            size=len(batch),
        ):
            embeddings = _active_model.encode(
                batch,
                batch_size=BATCH_SIZE,
                normalize_embeddings=True,
                show_progress_bar=False,
            )

            all_embeddings.extend(
                embeddings.tolist()
            )

    return all_embeddings