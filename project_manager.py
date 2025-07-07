"""
Project manager for handling multiple RAG projects
"""
import os
import importlib.util
from typing import Dict, List
from base_project import BaseProject


class ProjectManager:
    """Manages multiple projects and their vector stores"""
    
    def __init__(self, projects_dir: str = "./projects"):
        self.projects_dir = projects_dir
        self.projects: Dict[str, BaseProject] = {}
        self.retrievers: Dict[str, any] = {}
        
    def discover_projects(self) -> List[str]:
        """Discover all project directories"""
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)
            return []
            
        projects = []
        for item in os.listdir(self.projects_dir):
            project_path = os.path.join(self.projects_dir, item)
            if os.path.isdir(project_path):
                required_files = ["data.csv", "prompt.txt", "project.py"]
                if all(os.path.exists(os.path.join(project_path, f)) for f in required_files):
                    projects.append(item)
        return projects
    
    def load_project(self, project_name: str) -> BaseProject:
        """Load a project class from its project.py file"""
        project_dir = os.path.join(self.projects_dir, project_name)
        project_file = os.path.join(project_dir, "project.py")
        
        # Dynamically import the project module
        spec = importlib.util.spec_from_file_location(f"{project_name}_project", project_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find the project class (should inherit from BaseProject)
        project_class = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and 
                issubclass(attr, BaseProject) and 
                attr != BaseProject):
                project_class = attr
                break
        
        if not project_class:
            raise ValueError(f"No BaseProject subclass found in {project_file}")
        
        return project_class(project_name, project_dir)

    def initialize_all_projects(self, force_refresh: bool = False):
        """Load all discovered projects, optionally create/refresh vector stores"""
        project_names = self.discover_projects()
        for project_name in project_names:
            try:
                print(f"Loading project: {project_name}")
                project = self.load_project(project_name)
                self.projects[project_name] = project
                print(f"✓ Successfully loaded project: {project_name}")
                if force_refresh:
                    self.create_vector_store(project_name, force_refresh=True)
            except Exception as e:
                print(f"✗ Failed to load project {project_name}: {e}")

    def create_vector_store(self, project_name: str, force_refresh: bool = False):
        """Create or refresh vector store for a single project on demand."""
        if project_name not in self.projects:
            self.projects[project_name] = self.load_project(project_name)
        project = self.get_project(project_name)
        retriever = project.create_vector_store(force_refresh=force_refresh)
        self.retrievers[project_name] = retriever
        print(f"✓ Vector store {'refreshed' if force_refresh else 'created'} for project: {project_name}")


    def get_project(self, project_name: str) -> BaseProject:
        """Get a loaded project"""
        if project_name not in self.projects:
            raise ValueError(f"Project {project_name} not loaded")
        return self.projects[project_name]

    def get_retriever(self, project_name: str):
        if project_name not in self.retrievers:
            self.create_vector_store(project_name)
        return self.retrievers[project_name]
    
    def list_projects(self) -> List[str]:
        """List all available projects"""
        return list(self.projects.keys())

    def refresh_project(self, project_name: str):
        """Explicitly refresh vector store for a single project."""
        self.create_vector_store(project_name, force_refresh=True)
