"""
Test script for the multi-project RAG system
"""
from project_manager import ProjectManager
from langchain_ollama.llms import OllamaLLM


def test_multi_project_system():
    """Test the multi-project system functionality"""
    
    print("Testing Multi-Project RAG System")
    print("=" * 40)
    
    # Initialize project manager
    pm = ProjectManager()
    
    # Discover projects
    projects = pm.discover_projects()
    print(f"Discovered projects: {projects}")
    
    # Initialize projects (using existing vector stores)
    print("\nInitializing projects...")
    pm.initialize_all_projects(force_refresh=False)
    
    # Test each project
    model = OllamaLLM(model="llama3.2")
    
    print("\n" + "=" * 40)
    print("Testing UX Maturity Project")
    print("=" * 40)
    
    try:
        ux_project = pm.get_project("ux_maturity")
        ux_retriever = pm.get_retriever("ux_maturity")
        ux_prompt = ux_project.get_prompt_template()
        
        # Test query
        question = "What are the key factors that influence UX maturity in academic libraries?"
        docs = ux_retriever.invoke(question)
        context = "\n".join([doc.page_content for doc in docs])
        
        chain = ux_prompt | model
        result = chain.invoke({"responses": context, "question": question})
        
        print(f"Question: {question}")
        print(f"Retrieved {len(docs)} relevant documents")
        print(f"Answer: {result[:200]}...")
        
    except Exception as e:
        print(f"Error testing UX Maturity project: {e}")
    
    print("\n" + "=" * 40)
    print("Testing LCSH Variant Labels Project")
    print("=" * 40)
    
    try:
        lcsh_project = pm.get_project("lcsh_variant_labels")
        lcsh_retriever = pm.get_retriever("lcsh_variant_labels")
        lcsh_prompt = lcsh_project.get_prompt_template()
        
        # Test query
        question = "library automation systems"
        docs = lcsh_retriever.invoke(question)
        candidate_labels = [doc.page_content for doc in docs]
        formatted_labels = "\n".join(f"- {label}" for label in candidate_labels)
        
        chain = lcsh_prompt | model
        result = chain.invoke({"responses": formatted_labels, "question": question})
        
        print(f"Question: {question}")
        print(f"Retrieved {len(docs)} candidate labels")
        print("Sample labels:")
        for i, label in enumerate(candidate_labels[:3], 1):
            print(f"  {i}. {label}")
        print(f"Answer: {result[:200]}...")
        
    except Exception as e:
        print(f"Error testing LCSH project: {e}")
    
    print("\n" + "=" * 40)
    print("Testing Restaurant Reviews Project")
    print("=" * 40)
    
    try:
        restaurant_project = pm.get_project("restaurant_reviews")
        restaurant_retriever = pm.get_retriever("restaurant_reviews")
        restaurant_prompt = restaurant_project.get_prompt_template()
        
        # Test query
        question = "What do customers say about service quality?"
        docs = restaurant_retriever.invoke(question)
        context = "\n".join([doc.page_content for doc in docs])
        
        chain = restaurant_prompt | model
        result = chain.invoke({"responses": context, "question": question})
        
        print(f"Question: {question}")
        print(f"Retrieved {len(docs)} relevant reviews")
        print(f"Answer: {result[:200]}...")
        
    except Exception as e:
        print(f"Error testing Restaurant Reviews project: {e}")
    
    print("\n" + "=" * 40)
    print("All tests completed!")


if __name__ == "__main__":
    test_multi_project_system()
