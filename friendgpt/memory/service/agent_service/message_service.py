from neo4j import Transaction

from friendgpt.memory.db.type.cognition import Neo4jCognition


def agent_message_add_service(tx: Transaction, content: str, messages: list[Neo4jCognition]):
    """

    :param tx:
    :param content:
    :param messages:
    :return:
    """
