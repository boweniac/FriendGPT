from neo4j import Transaction
from typing_extensions import LiteralString

from friendgpt.memory.db.type.message_type import Neo4jMessage, Neo4jMessageWithBranch


# 客户端服务
# --对话中，最新一条消息的id
# - 对话中，聊天记录（分页）
# 系统服务
# - 判断，新消息与前序消息的关联度
# - 按事件聚类消息
# - 总结事件
# - 匹配事件
# - 根据事件关联的经验，总结新的经验
# - 匹配并关联经验与事件
# - 追加新的消息

# 事件
# - es：事件向量&文本
# - neo4j：事件节点 & 事件-消息关系
# 消息
# - neo4j：消息节点（包括内容）
# - mysql：思考过程

# 经验
# - es：经验向量&文本
# - neo4j：经验节点 & 经验-事件关系


def neo4j_message_add_operation(tx: Transaction, parent_id: int, message: Neo4jMessage):
    """
    添加消息
    :param tx: 事务
    :param parent_id:
    :param message:
    :return:
    """
    # created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    # message = create_message(msg_id, chat_id, sender_id, content)
    query: LiteralString = """
        MERGE (parent_message:Message {id: $parent_id})
        CREATE (new_message:Message $new_message)
        CREATE (parent_message)-[:LINK_MESSAGE]->(new_message)
        """
    parameters = {
        'parent_id': parent_id,
        'new_message': message
    }

    tx.run(query, **parameters)


def neo4j_message_get_last_message_id_operation(tx: Transaction, msg_id: int) -> int:
    """
    获取最后一条消息的 id
    :param tx:
    :param msg_id: 对话中任意消息 id
    :return: 同对话最后一条消息的 id
    """
    query: LiteralString = """
            MATCH (message:Message {id: $msg_id})-[:LINK_MESSAGE*]->(last_message)
            WHERE NOT (last_message)-[:LINK_MESSAGE]->()
            RETURN last_message.id
            ORDER BY last_message.created_at DESC
            LIMIT 1
            """
    parameters = {
        'msg_id': msg_id
    }
    results = tx.run(query, **parameters)
    return results.data()[0]['last_message.id']


def neo4j_get_previous_messages_operation(tx: Transaction, msg_id: int, limit: int) -> list[Neo4jMessageWithBranch]:
    """
     从指定消息节点开始，回溯 limit 条消息
    :param tx:
    :param msg_id:
    :param limit:
    :return:
    """
    query = f"""
            MATCH (:Message {{id: {msg_id}}})<-[:LINK_MESSAGE*0..{limit}]-(message)
            OPTIONAL MATCH (message)-[:LINK_MESSAGE]->(branch_message)
            WITH message, COLLECT(branch_message) AS branch_messages
            RETURN message, CASE WHEN SIZE(branch_messages) > 1 THEN branch_messages ELSE [] END AS branch_messages
            """
    results = tx.run(query)
    return results.data()
