from neo4j import GraphDatabase


class Neo4jClient:
    """
    Neo4j 服务
    """

    def __init__(
            self,
            config: dict
    ):
        self.client = GraphDatabase.driver(config["uri"],
                                           auth=(config["user"], config["pass"]))

    def __del__(self):
        """
        在实例引用数为 0 时，关闭数据库连接
        :return:
        """
        self.client.close()
