"""
Template Project - Replace this docstring and class name for your project
"""
import pandas as pd
import os
import sys
from pathlib import Path
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

# Add parent directory to path to import base_project
sys.path.append(str(Path(__file__).parent.parent.parent))
from base_project import BaseProject


class TemplateProject(BaseProject):
    """Template project class - rename for your project"""
    
    def process_row(self, row: pd.Series, index: int) -> Document:
        """Process a row from data.csv and return a Document object. Edit this for your data schema."""
        # Example: Use a column as main content, others as metadata
        page_content = str(row.get('main_content', ''))
        metadata = {k: str(v) for k, v in row.items() if k != 'main_content'}
        # Clean up metadata - remove empty or 'nan' values
        metadata = {k: v for k, v in metadata.items() if v and v != 'nan' and str(v).strip()}
        return Document(page_content=page_content, metadata=metadata, id=str(index))
    
    def get_prompt_template(self) -> ChatPromptTemplate:
        """Load prompt template from file or use default. Edit the default for your project."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, 'r') as f:
                template = f.read()
        else:
            template = """
You are an expert in this domain. Use the provided data to answer the user's question.

Relevant data:
{responses}

Question: {question}

Provide a clear, concise, and well-structured answer using only the data above.
"""
        return ChatPromptTemplate.from_template(template)
    
    def get_batch_size(self) -> int:
        """Set batch size for your data (edit as needed)"""
        return 100
