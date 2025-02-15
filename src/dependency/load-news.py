import pandas as pd
from neo4j import GraphDatabase
from sentence_transformers import (
    SentenceTransformer,
)  # Replace with actual embedding library

data_source_path = "/Users/admin/Documents/Personal/fyp/mistai-agents/src/dependency/golden-copy-scraped-articles.xlsx"

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"
NEO4J_DATABASE = "neo4j"

# Initialize Neo4j driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Initialize Neo4j connection
# Initialize embedding model (replace with your embedding model)
embeddings = SentenceTransformer("all-MiniLM-L6-v2")


df = pd.read_excel(data_source_path, engine="openpyxl")
df = df.dropna(subset=["Content"])  # Specify engine="openpyxl" for .xlsx files


# Function to run queries
def run_query(driver, query):
    with open(
        "/Users/admin/Documents/Personal/fyp/mistai-agents/src/dependency/golden-copy.cql",
        "a",
    ) as file:
        file.write(f"{query}\n")
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]


# Function to split text into chunks
def split_text(text, chunk_size=500, overlap=0):
    if chunk_size < 1 or overlap < 0:
        raise ValueError("size must be >= 1 and overlap >= 0")

    for i in range(0, len(text) - overlap, chunk_size - overlap):
        yield text[i : i + chunk_size]


# Iterate through rows
for index, row in df.iterrows():
    news = row.to_dict()

    # **Step 1: Split Document into Chunks**
    chunks = split_text(news["Content"], chunk_size=1000, overlap=200)

    # **Step 2: Start the Loop Over Chunks**
    prev_node_id = None  # Initialize prev_node_id before the loop
    for i, chunk in enumerate(chunks):
        # Escape single quotes in the chunk text
        escaped_chunk = chunk.replace("'", "\\'")

        # **Step 3: Create the Chunk Node in Neo4j**
        query = f'''
      CREATE (d:Document {{
          chunkID: "{f"chunk_{i}"}",
          url: "{news["URL"]}",
          docID: "{index}",
          date: "{news["Date"]}",
          full_text: '{escaped_chunk}',
          embeddings: {embeddings.encode([chunk])[0].tolist()}}}
      )
      RETURN ID(d);
      '''

        result = run_query(driver, query)  # Run the query
        chunk_node_id = result[0]["ID(d)"]  # Get the created node ID

        # **Step 4: Link Chunks Sequentially in Graph**
        if prev_node_id is not None:
            query = f"""
          MATCH (c1:Document), (c2:Document)
          WHERE ID(c1) = {prev_node_id} AND ID(c2) = {chunk_node_id}
          CREATE (c1)-[:NEXT]->(c2)
          CREATE (c2)-[:PREV]->(c1)
          """
            run_query(driver, query)

        prev_node_id = chunk_node_id  # Update previous node ID for the next iteration
