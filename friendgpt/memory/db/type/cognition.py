from datetime import datetime
from typing import TypedDict


class Neo4jCognition(TypedDict):
    id: int
    owner_id: int
    friend_id: int
    type: int
    content: str
    created_at: str


def create_neo4j_cognition(cognition_id: int, owner_id: int, friend_id: int, type: int, content: str) -> Neo4jCognition:
    return {
        "id": cognition_id,
        "owner_id": owner_id,
        "friend_id": friend_id,
        "type": type,
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    }

