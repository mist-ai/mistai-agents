class QueryGenerator:
    @staticmethod
    def generate_sector_query(keyword):
        """
        Fetch sector names for a given keyword.
        :param keyword: str - Keyword to search for in sector names
        :return: str - Cypher query to fetch sector names
        """
        return f"""
        MATCH (s:Sector)
        WHERE (s.name CONTAINS "{keyword}" OR s.name CONTAINS "{keyword.split()[0]}")
        RETURN DISTINCT s.name AS name
        """
    
    @staticmethod
    def generate_company_query(keyword, sector=None):
        """
        Fetch company tickers and names for a given keyword, optionally filtering by sector.
        :param keyword: str - Keyword to search for in company names and tickers
        :param sector: str - Sector to filter by
        :return: str - Cypher query to fetch company tickers and names
        """
        query = f"""
        MATCH (c:Company)
        WHERE (toLower(c.name) CONTAINS "{keyword.lower()}" OR toLower(c.ticker) CONTAINS "{keyword.lower()}" OR toLower(c.name) CONTAINS "{keyword.lower().split()[0]}")
        """
        
        # if sector:
        #     query += " AND (c)-[:BELONGS_TO]->(:Sector {name: $sector})"
        
        query += "RETURN DISTINCT c.ticker AS ticker, c.name AS name"
        print(query)
        return query
    
    @staticmethod
    def get_companies_for_sector(sector):
        """
        Fetch companies for a given sector.
        :param sector: str - Sector name
        :return: str - Cypher query to fetch companies for a sector
        """
        return f"""
        MATCH (c:Company)-[:BELONGS_TO]->(s:Sector)
        WHERE toLower(s.name) CONTAINS "{sector}"
        RETURN DISTINCT c.ticker AS ticker, c.name AS name

        """

# Example usage
# print(QueryGenerator.get_company_info("John Keells Holdings"))