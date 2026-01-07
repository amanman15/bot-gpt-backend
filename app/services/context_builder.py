def build_context(history_messages, user_message: str):
    context = []

    # system prompt
    context.append({
        "role": "system",
        "content": "You are a helpful assistant."
    })

    # last N messages (sliding window)
    for msg in history_messages[-5:]:
        context.append({
            "role": msg.role,
            "content": msg.content
        })

    # current user message
    context.append({
        "role": "user",
        "content": user_message
    })

    return context
