from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
import shutil

def create_vector_store(csv_file, collection_name, force_refresh=False):
    """Create vector store from a CSV file
    Args:
        csv_file: Path to CSV file
        collection_name: Name of the collection
        force_refresh: If True, delete existing vector store and recreate
    """
    df = pd.read_csv(csv_file)
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    db_location = f"./chrome_langchain_db_{collection_name}"

    # Delete existing vector store if force_refresh is True
    if force_refresh and os.path.exists(db_location):
        print(f"Deleting existing vector store: {db_location}")
        shutil.rmtree(db_location)

    add_documents = not os.path.exists(db_location)

    # Rest of the function remains the same...
    if add_documents:
        documents = []
        ids = []

        if collection_name == "ux_maturity":
            for i, row in df.iterrows():
                page_content = f"Institution Type: {row['classification']} "
                if isinstance(row['reasons_for_stage_number'], str):
                    page_content += f"Comments: {row['reasons_for_stage_number']}"

                metadata = {
                    "stage": row["stage"],
                    "stage_bin": row["stage_bin"],
                    "total_methods": row["total_methods"]
                }
                documents.append(Document(page_content=page_content, metadata=metadata, id=str(i)))
                ids.append(str(i))

        elif collection_name == "restaurant_reviews":
            for i, row in df.iterrows():
                document = Document(
                    page_content=row["Title"] + " " + row["Review"],
                    metadata={"rating": row["Rating"], "date": row["Date"]},
                    id=str(i)
                )
                documents.append(document)
                ids.append(str(i))

    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory=db_location,
        embedding_function=embeddings
    )

    if add_documents:
        vector_store.add_documents(documents=documents, ids=ids)

    return vector_store.as_retriever(search_kwargs={"k": 5})

# Usage examples:
# Use existing vector store if available
#retriever = create_vector_store("uxmaturity2018_dataset_redacted.csv", "ux_maturity")

# Force refresh to recreate vector store
retriever = create_vector_store("uxmaturity2018_dataset_redacted.csv", "ux_maturity", force_refresh=True)