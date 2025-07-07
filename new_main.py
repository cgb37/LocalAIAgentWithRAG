"""
Multi-Project RAG Application
"""
from langchain_ollama.llms import OllamaLLM
from project_manager import ProjectManager
import re


class MultiProjectApp:
    """Main application handling multiple projects"""
    
    def __init__(self):
        self.model = OllamaLLM(model="llama3.2")
        self.project_manager = ProjectManager()
        self.current_project = None
        
    def initialize(self, force_refresh: bool = False):
        """Initialize all projects"""
        print("Initializing projects...")
        self.project_manager.initialize_all_projects(force_refresh=force_refresh)
        
        available_projects = self.project_manager.list_projects()
        if available_projects:
            print(f"Available projects: {', '.join(available_projects)}")
        else:
            print("No projects found. Please create projects in the ./projects directory.")
    
    def select_project(self, project_name: str):
        """Select active project"""
        if project_name in self.project_manager.list_projects():
            self.current_project = project_name
            print(f"Selected project: {project_name}")
        else:
            print(f"Project '{project_name}' not found.")
            print(f"Available projects: {', '.join(self.project_manager.list_projects())}")
    
    def query_current_project(self, question: str):
        """Query the currently selected project"""
        if not self.current_project:
            print("No project selected. Use 'select <project_name>' to choose a project.")
            return
        
        try:
            project = self.project_manager.get_project(self.current_project)
            retriever = self.project_manager.get_retriever(self.current_project)
            prompt_template = project.get_prompt_template()
            
            # Get relevant documents
            docs = retriever.invoke(question)
            context = "\n".join([doc.page_content for doc in docs])
            
            # Create chain and get response
            chain = prompt_template | self.model
            result = chain.invoke({"responses": context, "question": question})
            
            return result
        except Exception as e:
            print(f"Error querying project: {e}")
            return None
    
    def extract_llm_labels(self, llm_output, candidate_labels):
        """Extract only those candidate labels that appear in the LLM output (case-insensitive)"""
        selected = []
        for label in candidate_labels:
            # Use word boundary for exact match, fallback to substring if needed
            if re.search(rf"\\b{re.escape(label)}\\b", llm_output, re.IGNORECASE) or label in llm_output:
                selected.append(label)
        return selected
    
    def query_with_label_extraction(self, question: str):
        """Special query method for LCSH project that extracts specific labels"""
        if self.current_project != "lcsh_variant_labels":
            return self.query_current_project(question)
        
        try:
            retriever = self.project_manager.get_retriever(self.current_project)
            docs = retriever.invoke(question)
            candidate_labels = [doc.page_content for doc in docs]
            formatted_labels = "\\n".join(f"- {label}" for label in candidate_labels)
            
            project = self.project_manager.get_project(self.current_project)
            prompt_template = project.get_prompt_template()
            chain = prompt_template | self.model
            
            result = chain.invoke({"responses": formatted_labels, "question": question})
            selected_labels = self.extract_llm_labels(result, candidate_labels)
            
            print("LLM-selected subject headings from the database:")
            for i, label in enumerate(selected_labels, 1):
                print(f"{i}. {label}")
            print("\\nExplanation from LLM:\\n")
            
            return result
        except Exception as e:
            print(f"Error querying project: {e}")
            return None
    
    def run_interactive(self):
        """Run interactive mode"""
        print("Multi-Project RAG System")
        print("Commands:")
        print("  list - List available projects")
        print("  select <project_name> - Select a project")
        print("  refresh <project_name> - Refresh vector store for a project")
        print("  q - Quit")
        print()
        
        while True:
            if self.current_project:
                prompt_text = f"[{self.current_project}] Ask your question (or command): "
            else:
                prompt_text = "Enter command or select a project first: "
            
            user_input = input(prompt_text).strip()
            
            if user_input.lower() == "q":
                break
            elif user_input.lower() == "list":
                projects = self.project_manager.list_projects()
                if projects:
                    print(f"Available projects: {', '.join(projects)}")
                else:
                    print("No projects available.")
            elif user_input.lower().startswith("select "):
                project_name = user_input[7:].strip()
                self.select_project(project_name)
            elif user_input.lower().startswith("refresh "):
                project_name = user_input[8:].strip()
                if project_name in self.project_manager.list_projects():
                    print(f"Refreshing vector store for {project_name}...")
                    self.project_manager.refresh_project(project_name)
                else:
                    print(f"Project '{project_name}' not found.")
            else:
                # Treat as a question for the current project
                if self.current_project == "lcsh_variant_labels":
                    result = self.query_with_label_extraction(user_input)
                else:
                    result = self.query_current_project(user_input)
                
                if result:
                    print("\n" + result + "\n")


def main():
    app = MultiProjectApp()
    app.initialize()
    app.run_interactive()


if __name__ == "__main__":
    main()
