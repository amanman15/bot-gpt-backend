def get_mock_context(conversation_id: int) -> str:
    """
    Simulated RAG retrieval.
    In production this would query embeddings / vector DB.
    """
    return (
        "BOT GPT is an internal conversational AI platform. "
        "It supports open chat and document-grounded conversations."
    )
