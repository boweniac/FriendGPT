import unittest

from friendgpt.memory.db.client.neo4j_client import Neo4jClient
from friendgpt.memory.db.operation.message_operation import neo4j_message_add_operation, \
    neo4j_message_get_last_message_id_operation, neo4j_get_previous_messages_operation
from friendgpt.memory.db.type.message_type import create_neo4j_message
from friendgpt.utils.json_util import dict_from_json


class TestMessage(unittest.TestCase):

    def test_neo4j_message_add_operation(self):
        config_dict = dict_from_json("LOCAL_DB_CONFIG", "../../../config")
        neo4j_client = Neo4jClient(config_dict['neo4j'])
        neo4j_session = neo4j_client.client.session()
        neo4j_tx = neo4j_session.begin_transaction()
        message1 = create_neo4j_message(1, 0, 1, "今天晚上吃什么？")
        message2 = create_neo4j_message(2, 0, 1, "吃麦当劳？")
        message3 = create_neo4j_message(3, 0, 1, "吃肯德基？")
        message4 = create_neo4j_message(4, 0, 1, "好啊那几点？")
        message5 = create_neo4j_message(5, 0, 1, "改吃麦当劳怎么样？")

        neo4j_message_add_operation(neo4j_tx, 0, message1)
        neo4j_message_add_operation(neo4j_tx, 1, message2)
        neo4j_message_add_operation(neo4j_tx, 1, message3)
        neo4j_message_add_operation(neo4j_tx, 2, message4)
        neo4j_message_add_operation(neo4j_tx, 3, message5)

        neo4j_tx.commit()

    def test_neo4j_message_get_last_message_id_operation(self):
        config_dict = dict_from_json("LOCAL_DB_CONFIG", "../../../config")
        neo4j_client = Neo4jClient(config_dict['neo4j'])
        neo4j_session = neo4j_client.client.session()
        neo4j_tx = neo4j_session.begin_transaction()

        record = neo4j_message_get_last_message_id_operation(neo4j_tx, 2)

        print(f"records: {record}")

        neo4j_tx.commit()

    def test_neo4j_get_previous_messages_operation(self):
        config_dict = dict_from_json("LOCAL_DB_CONFIG", "../../../config")
        neo4j_client = Neo4jClient(config_dict['neo4j'])
        neo4j_session = neo4j_client.client.session()
        neo4j_tx = neo4j_session.begin_transaction()

        records = neo4j_get_previous_messages_operation(neo4j_tx, 1, 20)
        record = records[0]
        print(f"records: {records}")
        print(f"records: {record['message']['content']}")

        neo4j_tx.commit()
