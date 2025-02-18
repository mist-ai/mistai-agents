import spacy
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"
NEO4J_DATABASE = "neo4j"

# initialize language model
nlp = spacy.load("en_core_web_md")

# add pipeline (declared through entry_points in setup.py)
nlp.add_pipe("entityLinker", last=True)

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD), max_connection_lifetime=3600*24*30, keep_alive=True, max_connection_pool_size=100)

embeddings = SentenceTransformer("all-MiniLM-L6-v2")


# Function to create spacyNode and relationship in Neo4j
def create_spacy_node_and_relationship(tx, doc_id, chunk_id, description):
    # Process description using SpaCy
    doc = nlp(description.replace("\n", ""))

    all_linked_entities = doc._.linkedEntities
    for ent in all_linked_entities:
        if ent.description is None:
            continue
        
        print(chunk_id)
        # Create spacyNode and relationship in the database
        spacy_node_query = (
            "CREATE (s:Entity {embedding: $embedding, label: $label, url: $url, description: $description}) "
            "WITH s "
            "MATCH (d:Document {chunkID: $chunk_id, docID: $doc_id}) "
            "MERGE (d)-[:HAS_ENTITY]->(s)"
        )

        print(spacy_node_query)

        # Execute query to create the SpacyNode and relationship
        tx.run(
            spacy_node_query,
            doc_id=doc_id,
            chunk_id=chunk_id,
            embedding=embeddings.encode([ent.description])[0].tolist(),
            label=ent.label,
            url=ent.url,
            description=ent.description,
        )


# Function to get all Document nodes and process them
def process_documents(driver):
    results = []
    with driver.session() as session:
        # Query to get all document nodes
        query = "MATCH (d:Document) RETURN d.chunkID AS chunk_id, d.docID AS doc_id, d.full_text AS description"

        # Iterate through each document node
        result = session.run(query)  # Run the query

        # Fetch all records before consuming them
        results = [record for record in result]
        
    for record in results:
        doc_id = record["doc_id"]
        chunk_id = record["chunk_id"]
        description = record["description"]
        print(f"Processing Document {doc_id} {chunk_id}")
        with driver.session() as session1:
            # Create SpacyNode and relationship for each document
            session1.execute_write(
                create_spacy_node_and_relationship, doc_id, chunk_id, description
            )
            


# Run the process
process_documents(driver)

# Close the Neo4j driver connection
driver.close()
