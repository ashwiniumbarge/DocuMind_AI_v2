from rag.embeddings import embedding_manager

print("Import successful")

vector = embedding_manager.embed_query("Machine Learning")

print("Embedding length:", len(vector))