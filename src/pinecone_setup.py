from pinecone import Pinecone, ServerlessSpec
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("pinecone_setup.log"),
        logging.StreamHandler()
    ]
)

def setup_pinecone(api_key, index_name, dimension=3072, metric="cosine", cloud="aws", region="us-east-1"):
    """
    Sets up the Pinecone index. Deletes the existing index if it exists and creates a new one.
    
    Args:
        api_key (str): Pinecone API key.
        index_name (str): Name of the Pinecone index.
        dimension (int): Dimension of the embeddings.
        metric (str): Metric to use for the index.
        cloud (str): Cloud provider.
        region (str): Region for the index.
    
    Returns:
        pinecone.Index: The initialized Pinecone index.
    """
    pc = Pinecone(api_key=api_key)
    logging.info(f"Connected to Pinecone.")

    # Check if the index already exists
    existing_indexes = [index.name for index in pc.list_indexes()]
    if index_name in existing_indexes:
        # If it exists, delete it
        pc.delete_index(index_name)
        logging.info(f"Deleted existing index: {index_name}")
        
        # Wait for the deletion to complete
        while index_name in [index.name for index in pc.list_indexes()]:
            logging.info(f"Waiting for index {index_name} to be deleted...")
            time.sleep(1)
    
    # Create a new index
    try:
        pc.create_index(
            name=index_name,
            dimension=dimension,  # Correct dimension for text-embedding-3-large
            metric=metric,
            spec=ServerlessSpec(cloud=cloud, region=region)
        )
        logging.info(f"Created new index: {index_name}")
    except Exception as e:
        logging.error(f"Failed to create Pinecone index {index_name}: {e}")
        raise
    
    # Wait for the index to be ready
    try:
        while not pc.describe_index(index_name).status['ready']:
            logging.info(f"Waiting for index {index_name} to be ready...")
            time.sleep(1)
        logging.info(f"Pinecone index {index_name} is ready.")
    except Exception as e:
        logging.error(f"Error while waiting for Pinecone index {index_name} to be ready: {e}")
        raise
    
    # Get the index
    index = pc.Index(index_name)
    logging.info(f"Initialized Pinecone index: {index_name}")
    return index