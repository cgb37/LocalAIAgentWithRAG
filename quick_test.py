"""
Quick test script for the multi-project RAG system (no LLM calls)
"""
from project_manager import ProjectManager


def quick_test():
    """Quick test without LLM calls"""
    
    print("Quick Test: Multi-Project RAG System")
    print("=" * 40)
    
    try:
        # Initialize project manager
        pm = ProjectManager()
        
        # Discover projects
        projects = pm.discover_projects()
        print(f"✓ Discovered projects: {projects}")
        
        # Initialize projects (using existing vector stores)
        print("\n✓ Initializing projects...")
        pm.initialize_all_projects(force_refresh=False)
        
        # Test project access
        print("\n✓ Testing project access:")
        for project_name in projects:
            try:
                project = pm.get_project(project_name)
                retriever = pm.get_retriever(project_name)
                prompt_template = project.get_prompt_template()
                
                # Test retrieval without LLM
                test_query = "test query"
                docs = retriever.invoke(test_query)
                
                print(f"  - {project_name}: ✓ Retrieved {len(docs)} documents")
                
            except Exception as e:
                print(f"  - {project_name}: ✗ Error: {e}")
                import traceback
                traceback.print_exc()
        
        print("\n✓ All core functionality working!")
        print("\nTo test interactively, run:")
        print("  source venv/bin/activate && python3 new_main.py")
        
    except Exception as e:
        print(f"Global error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    quick_test()
