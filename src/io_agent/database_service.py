import sys
import os
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

                
    def get_company_info(self, keyword, sector=None):
        """Fetch company tickers for a given keyword, optionally filtering by sector."""
        query = f"""
        MATCH (c:Company)
        WHERE (c.name CONTAINS "{keyword}" OR c.ticker CONTAINS "{keyword}" OR c.name CONTAINS "{keyword.split()[0]}")
        """  

        # If sector is provided, add the filter for sector
        if sector:
            query_with_sector = query + " AND (c)-[:BELONGS_TO]->(:Sector {name: $sector})"
            query_with_sector += " RETURN DISTINCT c.ticker AS ticker"
        else:
            query_with_sector = query + " RETURN DISTINCT c.ticker AS ticker"

        query_with_no_sector = query + " RETURN DISTINCT c.ticker AS ticker"  # Default query without sector filter

        with self.driver.session() as session:
            # First, try with the sector filter
            result = session.execute_read(lambda tx: tx.run(query_with_sector, keyword=keyword, sector=sector).values())
            
            # If no result found with the sector filter, try without sector filter
            if not result:
                result = session.execute_read(lambda tx: tx.run(query_with_no_sector, keyword=keyword).values())
            
        # Return the results without null values
        return [record[0] for record in result if record[0] is not None]


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