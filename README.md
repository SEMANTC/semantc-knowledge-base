# LLM-Powered Analytics for Xero (Expandable to Other Data Sources)

This project provides an LLM-powered analytics framework, currently focused on Xero accounting data but designed for future expansion to other data sources. It uses a RAG (Retrieval-Augmented Generation) knowledge base to support LLMs in constructing SQL queries and answering user prompts about financial data.

## Project Overview

The main purpose of this project is to:
1. Maintain a comprehensive knowledge base of data schemas, metadata, and sample queries.
2. Support LLM analytics by providing context for identifying relevant tables, columns, and calculations.
3. Enable automatic SQL query construction based on user prompts.
4. Allow for future expansion to include additional data sources beyond Xero.

## Project Structure

```
.
├── scripts/
│   ├── build_push.sh
│   └── ...
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── pinecone_setup.py
│   └── utils.py
├── knowledge_base/
│   ├── information_schema/
│   │   ├── xero_accounts.yaml
│   │   └── ...
│   ├── metadata/
│   │   ├── xero_enumeration_account_type.yaml
│   │   └── ...
│   └── queries/
│       └── sample_queries.yaml
└── README.md
```

## Components

### Scripts

- `build_push.sh`: Shell script for building and pushing a Docker image to Google Cloud Registry.

### Source Code

- `main.py`: Main script for processing YAML files, generating embeddings, and storing them in Pinecone.
- `pinecone_setup.py`: Module for setting up and configuring Pinecone index.
- `utils.py`: Utility functions for processing YAML files.

### Knowledge Base

The knowledge base is organized into three main categories:

1. **Information Schema**: Contains YAML files describing the structure of data tables.
   - Example: `xero_accounts.yaml`

2. **Metadata**: Includes enumeration files and other metadata related to the data model.
   - Example: `xero_enumeration_account_type.yaml`

3. **Queries**: Stores sample SQL queries for common operations.
   - Example: `sample_queries.yaml`

This structure allows LLMs to quickly retrieve relevant information when constructing SQL queries or answering user prompts.

## How It Works

1. The knowledge base is processed and embedded into a vector database (Pinecone).
2. When a user submits a prompt, the LLM uses the RAG system to retrieve relevant context from the knowledge base.
3. Based on this context, the LLM identifies the appropriate tables, columns, and calculations needed to answer the query.
4. The LLM constructs an SQL query using this information.
5. The query is executed, and the results are interpreted by the LLM to provide a human-readable answer to the user's prompt.

## Setup and Usage

1. Ensure all required environment variables are set (OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME).
2. Run `main.py` to process the knowledge base and store embeddings in Pinecone.
3. Implement the LLM query processing system (not included in this repository) that uses the embedded knowledge base to construct SQL queries and answer user prompts.

## Dependencies

- OpenAI API
- Pinecone
- LangChain
- PyYAML

## Expanding to New Data Sources

To add support for new data sources:

1. Create new YAML files in the `information_schema` directory describing the tables and columns of the new data source.
2. Add any necessary enumeration or metadata files to the `metadata` directory.
3. Include sample queries for the new data source in the `queries` directory.
4. Update the embedding process in `main.py` if necessary to handle any new file types or structures.
5. Retrain or fine-tune the LLM if required to understand the context of the new data source.

## Contributing

To contribute to this project, please add new YAML files to the appropriate directories in the knowledge base. Ensure that all YAML files are properly formatted and follow the established schema. When adding support for new data sources, please update the documentation accordingly.

