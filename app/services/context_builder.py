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

    system_prompt = '''You are a helpful assistant for a conversation chat applicattion
            Follow these rules:
            1. Dont hallucinate.
            2. If you find anything offensive give that in output that this is offensive.
            3. Use only information available in conversation context.
    '''

    if retrieved_context:
        system_prompt += (
            "\nUse the following context to answer accurately.\n\n"
            f"Context:\n{retrieved_context}"
        )

    context.append({
        "role": "system",
        "content": system_prompt
    })
    print("Total history messages:", len(history_messages))
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
    print("Final context sent to LLM:")
    for c in context:
        print(c)

    return context
