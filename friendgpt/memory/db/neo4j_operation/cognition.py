from neo4j import Transaction
from typing_extensions import LiteralString

from friendgpt.memory.db.type.cognition import Neo4jCognition


# 对话（包括思绪）
# 年、月、周、日总结

# 执行（回忆、对话、阅读、搜索）

# 经验（总结、更新、遗忘）

# 代办（总结、跟进、遗忘）


def neo4j_operation_cognition_add(tx: Transaction, parent_id: int, cognition: Neo4jCognition,
                                  is_related_to_parent: bool):
    """
    添加意识
    :param tx: 事务
    :param parent_id:
    :param cognition:
    :param is_related_to_parent:
    :return:
    """
    if is_related_to_parent:
        query: LiteralString = """
            MERGE (parent_cognition:Cognition {id: $parent_id})
            CREATE (new_cognition:Cognition $new_cognition)
            WITH parent_cognition, new_cognition
            CREATE (parent_cognition)-[:LINK_RELATED]->(new_cognition)
            """
    else:
        query: LiteralString = """
            MERGE (parent_cognition:Cognition {id: $parent_id})
            CREATE (new_cognition:Cognition $new_cognition)
            WITH parent_cognition, new_cognition
            CREATE (parent_cognition)-[:LINK_UNRELATED]->(new_cognition)
            """
    parameters = {
        'parent_id': parent_id,
        'new_cognition': cognition
    }

    tx.run(query, **parameters)


def neo4j_operation_cognition_get_last_id(tx: Transaction, cognition_id: int) -> int:
    """
    获取与某个意识节点，同归属的最后一个意识节点的 id
    :param tx: 事务
    :param cognition_id: 某个意识节点 id
    :return: 同归属的最后一个意识节点的 id
    """
    query: LiteralString = """
            MATCH (cognition:Cognition {id: $cognition_id})-[:LINK_RELATED|LINK_UNRELATED*]->(last_cognition)
            WHERE NOT (last_cognition)-[:LINK_RELATED|LINK_UNRELATED]->()
            RETURN last_cognition.id
            ORDER BY last_cognition.created_at DESC
            LIMIT 1
            """
    parameters = {
        'cognition_id': cognition_id
    }
    results = tx.run(query, **parameters)
    return results.data()[0]['last_cognition.id']


def neo4j_operation_cognition_get_previous(tx: Transaction, cognition_id: int, limit: int) -> list[Neo4jCognition]:
    """
     从指定意识节点开始，回溯 limit 个意识节点
    :param tx:
    :param cognition_id:
    :param limit:
    :return:
    """
    query = f"""
            MATCH (cognition:Cognition {{id: {cognition_id}}})<-[:LINK_RELATED|LINK_UNRELATED*0..{limit}]-(cognitions:Cognition)
            RETURN cognitions
            """
    results = tx.run(query)
    return [record['cognitions'] for record in results.data()]


def neo4j_operation_cognition_get_related_previous(tx: Transaction, cognition_id: int, limit: int) -> list[Neo4jCognition]:
    """
     从指定意识节点开始，回溯 limit 个意识节点
    :param tx:
    :param cognition_id:
    :param limit:
    :return:
    """
    query = f"""
            MATCH (cognition:Cognition {{id: {cognition_id}}})<-[:LINK_RELATED*0..{limit}]-(cognitions:Cognition)
            RETURN cognitions
            """
    results = tx.run(query)
    return [record['cognitions'] for record in results.data()]

