# Build the Docker image
docker build -t knowledge-base-processor .

# Run the Docker container using the .env file
docker run -it --env-file .env knowledge-base-processor

# Alternatively, run the Docker container with environment variables passed directly
# docker run -it -e OPENAI_API_KEY=your_openai_key -e PINECONE_API_KEY=your_pinecone_key -e PINECONE_INDEX_NAME=your_index_name knowledge-base-processor