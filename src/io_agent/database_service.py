import sys
import os
from neo4j import GraphDatabase

sys.path.append(os.environ["SYS_PATH"])
from io_agent.keywords_extraction import extractor
from io_agent.io_queries import QueryGenerator
from sentence_transformers import SentenceTransformer


class DatabaseService:
    def __init__(self):
        uri = os.environ["NEO4J_URI"]
        username = os.environ["NEO4J_USERNAME"]
        password = os.environ["NEO4J_PASSWORD"]

        if not uri or not username or not password:
            raise ValueError("Missing database credentials in .env file")

        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def run_query(self, query: str, parameters: dict = None):
        """
        Execute a Cypher query with optional parameters.
        :param query: str - Cypher query to run
        :param parameters: dict - Optional parameters for the query
        :return: list - Query results
        """
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return result.data()

    def get_entities_from_graph(self, prompt):
        """
        Get the corresponding entities for the keywords from the graph
        :param keywords: dict
        :return: dict of keywords with their entities
        """
        entities = {}
        keywords = extractor.extract(prompt)

        for keyword, label in keywords.items():
            query = QueryGenerator.generate_company_query(keyword)

            result = self.run_query(query)
            for record in result:
                company_name = record["name"]
                company_ticker = record["ticker"]
                # add to entities
                entities[keyword] = {
                    "company_name": company_name,
                    "ticker": company_ticker,
                }

        return entities

    def get_companies_for_sector(self, sector):
        """
        Fetch companies for a given sector.
        :param sector: str - Sector
        :return: dict - Companies in the sector
        """
        query = QueryGenerator.get_companies_for_sector(sector)
        result = self.run_query(query)
        companies = {record["name"]: record["ticker"] for record in result}
        return companies

    def get_news_for_topic(self, topic):
        """
        Fetch news for a given topic.
        :param topic: str
        :return: dict - news data
        """
        embeddings = SentenceTransformer("all-MiniLM-L6-v2")
        query = QueryGenerator.get_docs_for_topic(
            embeddings.encode([topic])[0].tolist(), topic=topic
        )
        return self.run_query(
            query=query,
            parameters=dict(user_query_emb=embeddings.encode([topic])[0].tolist()),
        )


db_service = DatabaseService()