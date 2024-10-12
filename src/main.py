# knowledge_base_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base')
import os
import logging
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from utils import iterate_yaml_files
from pinecone_setup import setup_pinecone
from tenacity import retry, stop_after_attempt, wait_random_exponential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("knowledge_base_main.log"),
        logging.StreamHandler()
    ]
)

load_dotenv()

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_embeddings(texts, embeddings):
    """
    Generate embeddings for the given texts using OpenAI's API.
    
    Args:
        texts (list): List of text chunks.
        embeddings (OpenAIEmbeddings): OpenAI Embeddings instance.
    
    Returns:
        list: List of embeddings.
    """
    try:
        return embeddings.embed_documents(texts)
    except Exception as e:
        logging.error(f"An error occurred during embedding generation: {e}")
        raise

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    pinecone_index_name = os.getenv('PINECONE_INDEX_NAME')

    if not all([openai_api_key, pinecone_api_key, pinecone_index_name]):
        logging.error("Please set all required environment variables: OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME.")
        raise ValueError("Missing required environment variables.")

    # Set OpenAI API key
    os.environ["OPENAI_API_KEY"] = openai_api_key
    logging.info("Set OpenAI API key.")

    # Initialize embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    logging.info("Initialized OpenAI embeddings with model 'text-embedding-3-large'.")

    # Setup Pinecone
    index = setup_pinecone(pinecone_api_key, pinecone_index_name, dimension=3072)
    logging.info("Pinecone setup completed.")

    # Create vector store
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    logging.info("Initialized PineconeVectorStore.")

    # Define knowledge base directory
    knowledge_base_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'semantic_layer')
    logging.info(f"Knowledge base directory: {knowledge_base_dir}")

    for yaml_content in iterate_yaml_files(knowledge_base_dir, reformat=True):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(yaml_content)
        logging.info(f"Splitting text into {len(texts)} chunks.")
        embedded_texts = generate_embeddings(texts, embeddings)
        vector_store.add_texts(texts, embeddings=embedded_texts)
        logging.info("Added texts to Pinecone vector store.")

    logging.info("All YAML files processed and stored in Pinecone.")

if __name__ == "__main__":
    main()