import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from utils import iterate_yaml_files
from pinecone_setup import setup_pinecone

load_dotenv()

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    pinecone_index_name = os.getenv('PINECONE_INDEX_NAME')

    if not all([openai_api_key, pinecone_api_key, pinecone_index_name]):
        raise ValueError("Please set all required environment variables.")

    embeddings = OpenAIEmbeddings()
    index = setup_pinecone(pinecone_api_key, pinecone_index_name)

    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    knowledge_base_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base')
    for yaml_content in iterate_yaml_files(knowledge_base_dir):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        # print(yaml_content)
        texts = text_splitter.split_text(yaml_content)

        vector_store.add_texts(texts)

    print("All YAML files processed and stored in Pinecone")

if __name__ == "__main__":
    main()