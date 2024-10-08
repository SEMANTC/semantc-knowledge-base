from pinecone import Pinecone, ServerlessSpec

def setup_pinecone(api_key, index_name):
    pc = Pinecone(api_key=api_key)

    # check if the index already exists
    existing_indexes = [index.name for index in pc.list_indexes()]
    
    if index_name not in existing_indexes:
        # if not, create it
        pc.create_index(
            name=index_name,
            dimension=1536,  # OpenAI embeddings are 1536 dimensions
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    # get the index
    index = pc.Index(index_name)
    return index