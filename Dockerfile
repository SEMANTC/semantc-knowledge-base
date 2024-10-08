FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY knowledge_base/ /app/knowledge_base/

ENV OPENAI_API_KEY=""
ENV PINECONE_API_KEY=""
ENV PINECONE_INDEX_NAME=""

CMD ["python", "src/main.py"]