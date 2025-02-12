import sys
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
sys.path.append(os.environ["SYS_PATH"])


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

    def get_company_info(self, sector, keyword):
        """Fetch company tickers for a given sector and keyword."""
        query = """
        MATCH (c:Company)-[:BELONGS_TO]->(s:Sector {name: $sector})
        WHERE c.name CONTAINS $keyword OR c.ticker CONTAINS $keyword
        RETURN c.ticker AS ticker
        """
        with self.driver.session() as session:
            result = session.execute_read(lambda tx: tx.run(query, sector=sector, keyword=keyword).values())
            return [record[0] for record in result] 
        
    # # Get the news articles for a given keyword
    # def get_news_articles(self, keyword):
    #     """Fetch news articles related to a given keyword."""
    #     query = """
    #     MATCH (n:NewsArticle)
    #     WHERE n.keywords CONTAINS $keyword
    #     RETURN n.title AS title, n.source AS source, n.content AS content, n.date AS date
    #     """
    #     with self.driver.session() as session:
    #         result = session.execute_read(lambda tx: tx.run(query, keyword=keyword).values())
    #         return [{"title": record[0], "source": record[1], "content": record[2], "date": record[3]} for record in result]


db_service = DatabaseService()