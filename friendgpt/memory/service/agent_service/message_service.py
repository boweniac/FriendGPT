from neo4j import Transaction

from friendgpt.memory.db.type.message_type import Neo4jMessage


def agent_message_add_service(tx: Transaction, content: str, messages: list[Neo4jMessage]):
    """

    :param tx:
    :param content:
    :param messages:
    :return:
    """
