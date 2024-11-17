import unittest

from friendgpt.memory.db.client.neo4j_client import Neo4jClient
from friendgpt.memory.db.neo4j_operation.cognition import neo4j_operation_cognition_add, \
    neo4j_operation_cognition_get_last_id, neo4j_operation_cognition_get_previous, \
    neo4j_operation_cognition_get_related_previous
from friendgpt.memory.db.type.cognition import create_neo4j_cognition
from friendgpt.utils.json_util import dict_from_json


class TestMessage(unittest.TestCase):

    def test_neo4j_operation_cognition_add(self):
        config_dict = dict_from_json("LOCAL_DB_CONFIG", "../../../config")
        neo4j_client = Neo4jClient(config_dict['neo4j'])
        neo4j_session = neo4j_client.client.session()
        neo4j_tx = neo4j_session.begin_transaction()
        message1 = create_neo4j_cognition(1, 1, 2, 2, "今天晚上吃什么？")
        message2 = create_neo4j_cognition(2, 1, 1, 2, "吃麦当劳？")
        message3 = create_neo4j_cognition(3, 1, 2, 2, "吃肯德基？")
        message4 = create_neo4j_cognition(4, 1, 1, 2, "好啊那几点？")
        message5 = create_neo4j_cognition(5, 1, 2, 2, "今天下雨吗")
        message6 = create_neo4j_cognition(6, 1, 1, 2, "好像不下雨")
        message7 = create_neo4j_cognition(7, 1, 2, 2, "改吃麦当劳怎么样？")
        message8 = create_neo4j_cognition(8, 1, 1, 2, "我都可以你定吧")
        message9 = create_neo4j_cognition(9, 1, 2, 2, "那就5点吃麦当劳")

        neo4j_operation_cognition_add(neo4j_tx, 0, message1, False)
        neo4j_operation_cognition_add(neo4j_tx, 1, message2, True)
        neo4j_operation_cognition_add(neo4j_tx, 2, message3, True)
        neo4j_operation_cognition_add(neo4j_tx, 3, message4, True)
        neo4j_operation_cognition_add(neo4j_tx, 4, message5, False)
        neo4j_operation_cognition_add(neo4j_tx, 5, message6, True)
        neo4j_operation_cognition_add(neo4j_tx, 6, message7, False)
        neo4j_operation_cognition_add(neo4j_tx, 7, message8, True)
        neo4j_operation_cognition_add(neo4j_tx, 8, message9, True)

        neo4j_tx.commit()

    def test_neo4j_operation_cognition_get_last_id(self):
        config_dict = dict_from_json("LOCAL_DB_CONFIG", "../../../config")
        neo4j_client = Neo4jClient(config_dict['neo4j'])
        neo4j_session = neo4j_client.client.session()
        neo4j_tx = neo4j_session.begin_transaction()

        record = neo4j_operation_cognition_get_last_id(neo4j_tx, 2)

        print(f"records: {record}")

        neo4j_tx.commit()

    def test_neo4j_operation_cognition_get_previous(self):
        config_dict = dict_from_json("LOCAL_DB_CONFIG", "../../../config")
        neo4j_client = Neo4jClient(config_dict['neo4j'])
        neo4j_session = neo4j_client.client.session()
        neo4j_tx = neo4j_session.begin_transaction()

        records = neo4j_operation_cognition_get_previous(neo4j_tx, 9, 20)
        record = records[0]
        print(f"records: {records}")
        print(f"record: {record}")

        neo4j_tx.commit()

    def test_neo4j_operation_cognition_get_related_previous(self):
        config_dict = dict_from_json("LOCAL_DB_CONFIG", "../../../config")
        neo4j_client = Neo4jClient(config_dict['neo4j'])
        neo4j_session = neo4j_client.client.session()
        neo4j_tx = neo4j_session.begin_transaction()

        records = neo4j_operation_cognition_get_related_previous(neo4j_tx, 9, 20)
        record = records[0]
        print(f"records: {records}")
        print(f"record: {record}")

        neo4j_tx.commit()