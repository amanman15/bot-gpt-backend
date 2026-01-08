# def build_context(history_messages, user_message: str):
#     context = []

#     # system prompt
#     context.append({
#         "role": "system",
#         "content": "You are a helpful assistant."
#     })

#     # last N messages (sliding window)
#     for msg in history_messages[-5:]:
#         context.append({
#             "role": msg.role,
#             "content": msg.content
#         })

#     # current user message
#     context.append({
#         "role": "user",
#         "content": user_message
#     })

#     return context

def build_context(
    history_messages,
    user_message: str,
    retrieved_context: str | None = None
):
    context = []

    system_prompt = "You are a helpful assistant."

    if retrieved_context:
        system_prompt += (
            "\nUse the following context to answer accurately.\n\n"
            f"Context:\n{retrieved_context}"
        )

    context.append({
        "role": "system",
        "content": system_prompt
    })

    # last N messages (sliding window)
    for msg in history_messages[-5:]:
        context.append({
            "role": msg.role,
            "content": msg.content
        })

    context.append({
        "role": "user",
        "content": user_message
    })

    return context
