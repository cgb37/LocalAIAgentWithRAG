from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are an expert in analyzing UX maturity and research methods in academic libraries.
Focus on providing insights about UX practices, maturity stages, and research methods used in university libraries.

Here is relevant data from the UX maturity assessment: {responses}

Based on this data, please answer the following question: {question}

Keep your analysis focused on:
- UX maturity stages and progression
- Research methods and their effectiveness
- Institutional characteristics and their impact
- Challenges and success factors in UX implementation
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n-------------------------------")
    question = input("Ask your question about library UX (q to quit): ")
    print("\n\n")
    if question == "q":
        break

    context = retriever.invoke(question)
    result = chain.invoke({"responses": context, "question": question})
    print(result)