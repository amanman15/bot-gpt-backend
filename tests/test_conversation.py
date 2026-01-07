def test_start_conversation(client):
    response = client.post(
        "/conversations/",
        json={"user_id": 1, "message": "Hello"}
    )
    assert response.status_code == 200
    assert "conversation_id" in response.json()


def test_get_conversation(client):
    # First create conversation
    response = client.post(
        "/conversations/",
        json={"user_id": 1, "message": "Hello"}
    )
    conversation_id = response.json()["conversation_id"]

    # Then fetch conversation
    response = client.get(f"/conversations/{conversation_id}")
    assert response.status_code == 200
    assert "messages" in response.json()
    assert "conversation_id" in response.json()
