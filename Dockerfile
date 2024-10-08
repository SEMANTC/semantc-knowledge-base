# Dockerfile for LangChain with Pinecone and Google Cloud Run
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ /app/src/
COPY knowledge_base/ /app/knowledge_base/

CMD ["python", "src/main.py"]