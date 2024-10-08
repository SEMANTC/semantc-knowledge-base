# LangChain with Pinecone and Google Cloud Run

This project demonstrates how to use LangChain with Pinecone for vector storage and Google Cloud Run for deployment. The application processes YAML files from a Google Cloud Storage bucket, splits the text into chunks, and stores the chunks in a Pinecone index.

## Project Structure

```
.DS_Store
.env
.gitignore
Dockerfile
knowledge_base/
    xero_invoices.yaml
README.md
requirements.txt
src/
    __init__.py
    main.py
    pinecone_setup.py
    utils.py
```

## Prerequisites

- Python 3.9
- Docker
- Google Cloud SDK
- Pinecone API Key
- OpenAI API Key

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a [`.env`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Ffernandomaximoferreira%2Fsrc%2Ftext2sql-knowledge-base%2F.env%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%229e4555d6-befb-485c-9736-18594b759a56%22%5D "/Users/fernandomaximoferreira/src/text2sql-knowledge-base/.env") file in the root directory and add the following variables:

    ```env
    OPENAI

_API

_KEY=<your-openai-api-key>
    PINECONE_API_KEY=<your-pinecone-api-key>
    PINECONE_INDEX_NAME=<your-pinecone-index-name>
    ```

## Running the Application

1. **Run the application locally:**

    ```sh
    python src/main.py
    ```

2. **Build and run the Docker container:**

    ```sh
    docker build -t langchain-app .
    docker run -p 8080:8080 langchain-app
    ```

## Deployment to Google Cloud Run

1. **Build the Docker image:**

    ```sh
    gcloud builds submit --tag gcr.io/<your-project-id>/langchain-app
    ```

2. **Deploy to Cloud Run:**

    ```sh
    gcloud run deploy --image gcr.io/<your-project-id>/langchain-app --platform managed
    ```

## Code Overview

- **[`src/main.py`]**: Main entry point of the application. It sets up OpenAI and Pinecone, processes YAML files, and stores the text chunks in Pinecone.
- **[`src/pinecone_setup.py`]**: Contains the function to set up Pinecone.
- **[`src/utils.py`]**: Utility functions, including iterating over YAML files in the knowledge base directory.

