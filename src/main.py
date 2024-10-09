import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from utils import iterate_yaml_files
from pinecone_setup import setup_pinecone
from tenacity import retry, stop_after_attempt, wait_random_exponential

load_dotenv()

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_embeddings(texts, embeddings):
    try:
        return embeddings.embed_documents(texts)
    except Exception as e:
        print(f"an error occurred: {e}")
        raise

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    pinecone_index_name = os.getenv('PINECONE_INDEX_NAME')

    if not all([openai_api_key, pinecone_api_key, pinecone_index_name]):
        raise ValueError("please set all required environment variables.")

    # Set OpenAI API key
    os.environ["OPENAI_API_KEY"] = openai_api_key

    # Initialize embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # Setup Pinecone
    index = setup_pinecone(pinecone_api_key, pinecone_index_name)

    # Create vector store
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    knowledge_base_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base')
    for yaml_content in iterate_yaml_files(knowledge_base_dir, reformat=True):
    # for yaml_content in iterate_yaml_files(knowledge_base_dir):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(yaml_content)
        print(knowledge_base_dir)
        embedded_texts = generate_embeddings(texts, embeddings)
        vector_store.add_texts(texts, embeddings=embedded_texts)

    print("all YAML files processed and stored in Pinecone")

if __name__ == "__main__":
    main()