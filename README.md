# Local AI Agent with RAG

LocalAIAgentWithRAG is a local implementation of an Artificial Intelligence (AI) Agent utilizing 
Retrieval-Augmented Generation (RAG) to enhance context-aware responses by leveraging 
external knowledge sources.

This project is designed to keep everything running locally, ensuring better data privacy and 
low-latency inference. It is perfect for applications requiring local knowledge search and 
processing in combination with generative AI.


## Project Description: Library RAG System with Open Source LLMs
This project demonstrates how libraries can leverage open-source AI technologies to create powerful 
information retrieval systems for specialized collections and datasets.
Using Ollama (a local LLM runner), Langchain (an AI application framework), 
and open-source language models, we've built a Retrieval-Augmented Generation (RAG) system 
that can answer nuanced questions about library datasets - in this case, user experience research in academic libraries.
The system combines the analytical power of pandas for data handling with the contextual understanding 
of large language models to provide accurate, evidence-based responses to complex queries about your data.

### Key features:

- Runs completely locally - no data sent to external APIs
- Uses free, open-source models (Llama 3.2 and MX Embeddings)
- Integrates with existing library datasets
- Provides sourced, relevant answers to natural language questions

This approach can be applied to various library collections, research datasets, and institutional repositories to improve discovery and insight generation.


## Features

- **Local Execution**: Ensures maximum data security and privacy by executing all processes locally without relying on external servers.
- **Retrieval-Augmented Generation (RAG)**: Combines generative AI with a document retrieval mechanism to provide contextually accurate responses based on input queries.
- **Extensible Architecture**: Easily adaptable to additional knowledge sources and algorithms.
- **Support for Popular Models**: Preloaded with AI models like `llama3.2` for RAG and `mxbai-embed-large` for embeddings.
- **Python Environment**: Simple Python-based environment setup using `venv`.

---

## Prerequisites

Before starting the project, make sure you have the following installed:

1. **Python 3.8 or Higher**: The project is built with Python, and a version >= 3.8 is recommended.
2. **Pip**: A package manager for Python.
3. **ollama CLI**: Needed to download and set up local AI models. You can find details [here](https://ollama.com/).
4. **Basic Knowledge Sources (Optional)**: Documents or databases that can supply the additional context required for your RAG pipeline.

---

## Installation Setup

The install script will:
- Create Python virtual environment
- Install required packages
- Download required AI models

The install script automates the setup process and includes error checking.
If you see green success messages, the installation is complete.


Follow these instructions to set up the project:

```markdown
2. Clone and install the project:
```shell script
git clone git@github.com:cgb37/LocalAIAgentWithRAG.git
cd LocalAIAgentWithRAG
```

3. Download and install Ollama:
    - Visit https://ollama.com/download
    - Download the Mac version
    - Double-click the downloaded file to install
    - Open Terminal and verify installation:
```shell script
ollama --version
```

4. Set the installation script to executable:
```shell script
chmod +x install.sh
```

5. Run the installation script:
```shell script
./install.sh
```


## Usage

Once the setup is complete, you can begin using the local RAG-powered AI agent:

1. Activate the Python virtual environment:
```shell script
source venv/bin/activate
```

2. Launch the application (example command):
```shell script
python3 main.py
```

3. Start interacting with the agent by providing queries. For example, ask questions like:


The system will use the retrieval-augmented generation technique to fetch context, process it using the `llama3.2` model, and provide a highly contextualized response.


## Local Models

The project uses the following models provided by `ollama`:

- **Llama 3.2**: A powerful language model designed for generating contextual responses.
- **MXBAI Embed Large**: A large embedding model for document vectorization and similarity searches.

These models are downloaded and stored locally, ensuring low latency and data privacy.

---

## Key Components

- **Local RAG Pipeline**: The agent's pipeline integrates document retrieval, embedding generation, and natural language generation in a self-contained environment.
- **Model Orchestration**: Powered by `ollama`, enabling seamless integration of various language models.
- **Document Preprocessing**: Includes tokenization, vectorization, and contextual keyword extraction to improve the quality of knowledge retrieval.

---


## Key AI Concepts for Libraries

**Ollama**: A user-friendly tool that lets you run advanced AI language models on your own computer rather than in the cloud. 
Think of it like having your own personal AI assistant that works completely offline, 
keeping your data private and secure within your institution.

**Langchain**: A framework that helps connect AI models to other tools and data sources. 
It's like a toolkit that lets librarians combine AI with databases, search functions, and other systems to create 
customized applications without needing advanced programming skills.

**Open-source language models**: AI systems whose code is publicly available, allowing anyone to use, modify, and improve them without licensing fees:
- **langchain-ollama**: A connector that helps Langchain work smoothly with Ollama's local AI models
- **langchain-chroma**: A component that helps store and search through text using AI-friendly "vector" representations, 
- making it possible to find information based on meaning rather than just keywords

**Retrieval-Augmented Generation (RAG)**: A technique that enhances AI responses by first searching through your library's specific documents, 
then using that retrieved information to generate accurate, contextual answers. This is particularly valuable for libraries because it:
1. Grounds AI responses in your actual collection materials
2. Provides citations to source documents
3. Reduces fictional or "hallucinated" information
4. Lets you leverage your unique collections and expertise

Think of RAG as giving an AI assistant the ability to first consult your library's resources before answering a question, similar to how a reference librarian might check the catalog or databases before responding to a patron query.


---

## Future Plans

- Adding support for customized retrievers to enhance compatibility with enterprise-grade knowledge bases.
- Expanding to other generative models for domain-specific applications.
- Integrating a GUI or web-based interface for non-technical users.
- Enhancing document ingestion pipelines for real-time updates.

---



## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements

- Special thanks to the developers of the `ollama` CLI for enabling seamless local model integration.
- Inspired by ongoing advancements in retrieval-augmented generation and the open-source AI community.

---

Let me know if you'd like further improvements!