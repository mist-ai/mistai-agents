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
        WHERE (toLower(c.name) CONTAINS "{keyword.lower()}" OR toLower(c.description) contains "{keyword.lower()}" OR toLower(c.ticker) CONTAINS "{keyword.lower()}" OR toLower(c.name) CONTAINS "{keyword.lower().split()[0]}")
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
        WHERE toLower(s.name) CONTAINS "{sector.lower()}"
        RETURN DISTINCT c.ticker AS ticker, c.name AS name

        """
    

    @staticmethod
    def get_docs_for_topic(embedding, topic):
        return """
        CALL db.index.vector.queryNodes('test_index_company', 10, $user_query_emb)
        YIELD node AS vectorNode, score as vectorScore
        WITH vectorNode, vectorScore
        MATCH (d:Document)-[r]->(vectorNode)
        WITH DISTINCT vectorNode as e, d, r, r.cosineSimilarity as cosineSimilarity
        ORDER BY cosineSimilarity DESC
        WITH ID(e) as id, e.label as title,
            cosineSimilarity,
            e.description as description,
            head(collect(d.docID)) as document_id,
            head(collect(d.chunkID)) as chunkID,
            head(collect(d.full_text)) as document_text,
            reduce(mDot = 0.0, i IN range(0, size($user_query_emb) - 1) | mDot + $user_query_emb[i] * e.embeddings[i]) /
            (sqrt(reduce(mSq = 0.0, x IN $user_query_emb | mSq + x^2)) * sqrt(reduce(eSq = 0.0, y IN e.embeddings | eSq + y^2))) AS entity_similarity,
            reduce(mDot = 0.0, i IN range(0, size($user_query_emb) - 1) | mDot + $user_query_emb[i] * d.embeddings[i]) /
            (sqrt(reduce(mSq = 0.0, x IN $user_query_emb | mSq + x^2)) * sqrt(reduce(dSq = 0.0, y IN d.embeddings | dSq + y^2))) AS document_similarity
        WITH id, title, description, document_id, document_text, entity_similarity, document_similarity, chunkID,
            (entity_similarity + document_similarity) / 2 AS similarity, cosineSimilarity
        WHERE similarity > 0.7
        RETURN id, title, document_id, document_text, similarity, chunkID
        ORDER BY cosineSimilarity DESC, similarity DESC
        """

# Example usage
# print(QueryGenerator.get_company_info("John Keells Holdings"))