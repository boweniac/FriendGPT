from datetime import datetime
from typing import TypedDict


class Neo4jMessage(TypedDict):
    id: int
    chat_id: int
    sender_id: int
    content: str
    created_at: str


def create_neo4j_message(msg_id: int, chat_id: int, sender_id: int, content: str) -> Neo4jMessage:
    return {
        "id": msg_id,
        "chat_id": chat_id,
        "sender_id": sender_id,
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    }


class Neo4jMessageWithBranch(TypedDict):
    message: Neo4jMessage
    branch_messages: list[Neo4jMessage]
