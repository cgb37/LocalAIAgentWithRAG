from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import lcsh_variant_retriever
import re

model = OllamaLLM(model="llama3.2")

template = """
You are an expert in library cataloging and subject analysis.
Given a description, select the most relevant Library of Congress Subject Headings (LCSH) variant labels from the list below.

Candidate LCSH variant labels:
{responses}

Description: {question}

Return a list of the most relevant subject headings from the candidates above, and explain your reasoning.
You must only return subject headings from the list above. Do not invent or modify any headings. If none are relevant, return an empty list.
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def extract_llm_labels(llm_output, candidate_labels):
    # Extract only those candidate labels that appear in the LLM output (case-insensitive)
    selected = []
    for label in candidate_labels:
        # Use word boundary for exact match, fallback to substring if needed
        if re.search(rf"\\b{re.escape(label)}\\b", llm_output, re.IGNORECASE) or label in llm_output:
            selected.append(label)
    return selected

while True:
    print("\n\n-------------------------------")
    question = input("Enter a description to find relevant LCSH subject headings (q to quit): ")
    print("\n\n")
    if question == "q":
        break

    docs = lcsh_variant_retriever.invoke(question)
    candidate_labels = [doc.page_content for doc in docs]
    formatted_labels = "\n".join(f"- {label}" for label in candidate_labels)

    result = chain.invoke({"responses": formatted_labels, "question": question})
    selected_labels = extract_llm_labels(result, candidate_labels)

    print("LLM-selected subject headings from the database:")
    for i, label in enumerate(selected_labels, 1):
        print(f"{i}. {label}")
    print("\nExplanation from LLM:\n")
    print(result)