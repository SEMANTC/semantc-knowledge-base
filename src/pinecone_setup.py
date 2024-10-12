from pinecone import Pinecone, ServerlessSpec
import time

def setup_pinecone(api_key, index_name):
    pc = Pinecone(api_key=api_key)

    # Check if the index already exists
    existing_indexes = [index.name for index in pc.list_indexes()]
    
    if index_name in existing_indexes:
        # If it exists, delete it
        pc.delete_index(index_name)
        print(f"Deleted existing index: {index_name}")
        
        # Wait for the deletion to complete
        while index_name in [index.name for index in pc.list_indexes()]:
            time.sleep(1)
    
    # Create a new index
    pc.create_index(
        name=index_name,
        dimension=3072,  # OpenAI embeddings are 3072 dimensions
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f"Created new index: {index_name}")
    
    # Wait for the index to be ready
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
    
    # Get the index
    index = pc.Index(index_name)
    return index