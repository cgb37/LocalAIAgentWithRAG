"""
Demonstration script for the Multi-Project RAG System
"""
from project_manager import ProjectManager
from langchain_ollama.llms import OllamaLLM


def demonstrate_system():
    """Demonstrate the multi-project system with sample queries"""
    
    print("🚀 Multi-Project RAG System Demonstration")
    print("=" * 50)
    
    # Initialize system
    print("📊 Initializing system...")
    pm = ProjectManager()
    model = OllamaLLM(model="llama3.2")
    
    # Discover and load projects
    projects = pm.discover_projects()
    print(f"✅ Found {len(projects)} projects: {', '.join(projects)}")
    
    pm.initialize_all_projects(force_refresh=False)
    print("✅ All projects initialized")
    
    # Demonstrate each project
    demonstrations = [
        {
            "project": "ux_maturity",
            "question": "What institutional factors influence UX maturity?",
            "description": "Analyzing UX research practices in academic libraries"
        },
        {
            "project": "lcsh_variant_labels", 
            "question": "digital libraries and information systems",
            "description": "Finding relevant Library of Congress Subject Headings"
        },
        {
            "project": "restaurant_reviews",
            "question": "What aspects of dining experience do customers value most?",
            "description": "Analyzing customer sentiment in restaurant reviews"
        }
    ]
    
    for demo in demonstrations:
        print(f"\n📋 {demo['description']}")
        print("=" * 50)
        print(f"Project: {demo['project']}")
        print(f"Question: {demo['question']}")
        print("-" * 50)
        
        try:
            # Get project components
            project = pm.get_project(demo['project'])
            retriever = pm.get_retriever(demo['project'])
            prompt_template = project.get_prompt_template()
            
            # Retrieve relevant documents
            docs = retriever.invoke(demo['question'])
            print(f"📄 Retrieved {len(docs)} relevant documents")
            
            # Show sample retrieved content
            print("📝 Sample retrieved data:")
            for i, doc in enumerate(docs[:2], 1):
                content = doc.page_content
                if len(content) > 100:
                    content = content[:100] + "..."
                print(f"  {i}. {content}")
            
            # Note: In a real demo, you would call the LLM here
            # For this demo, we'll skip the LLM call to save time
            print("🤖 LLM processing would happen here...")
            print("✅ Query completed successfully")
            
        except Exception as e:
            print(f"❌ Error processing {demo['project']}: {e}")
    
    print(f"\n🎉 Demonstration completed!")
    print("\n📖 Usage:")
    print("  1. Run: source venv/bin/activate")
    print("  2. Run: python3 new_main.py")
    print("  3. Use commands: list, select <project>, ask questions, q")
    

if __name__ == "__main__":
    demonstrate_system()
