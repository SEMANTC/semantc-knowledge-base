import os
from langchain.vectorstores import Pinecone as LangchainPinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from utils import iterate_yaml_files
from pinecone_setup import setup_pinecone

def main():
    # set up OpenAI and Pinecone
    openai_api_key = os.getenv('OPENAI_API_KEY')
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    pinecone_index_name = os.getenv('PINECONE_INDEX_NAME')

    if not all([openai_api_key, pinecone_api_key, pinecone_index_name]):
        raise ValueError("Please set all required environment variables.")

    # initialize embeddings and Pinecone
    embeddings = OpenAIEmbeddings()
    index = setup_pinecone(pinecone_api_key, pinecone_index_name)

    # process YAML files
    knowledge_base_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base')
    for yaml_content in iterate_yaml_files(knowledge_base_dir):
        # split the content
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(yaml_content)

        # store in Pinecone
        LangchainPinecone.from_texts(texts, embeddings, index_name=pinecone_index_name)

    print("all YAML files processed and stored in Pinecone")

if __name__ == "__main__":
    main()