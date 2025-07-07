"""
Script to create project-specific files for each project
"""
import os
from pathlib import Path


def create_ux_maturity_project():
    """Create UX Maturity project files"""
    project_dir = Path("./projects/ux_maturity")
    
    # Create project.py
    project_py_content = '''"""
UX Maturity Project - Analyzes UX research maturity in academic libraries
"""
import pandas as pd
import os
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from base_project import BaseProject


class UXMaturityProject(BaseProject):
    """UX Maturity research project"""
    
    def process_row(self, row: pd.Series, index: int) -> Document:
        """Process UX maturity data row"""
        page_content = f"Institution Type: {row['classification']} "
        if isinstance(row['reasons_for_stage_number'], str):
            page_content += f"Comments: {row['reasons_for_stage_number']}"

        metadata = {
            "stage": row["stage"],
            "stage_bin": row["stage_bin"], 
            "total_methods": row["total_methods"]
        }
        
        return Document(page_content=page_content, metadata=metadata, id=str(index))
    
    def get_prompt_template(self) -> ChatPromptTemplate:
        """Load prompt template from file or use default"""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, 'r') as f:
                template = f.read()
        else:
            template = """
You are an expert in analyzing UX maturity and research methods in academic libraries.
Focus on providing insights about UX practices, maturity stages, and research methods used in university libraries.

Here is relevant data from the UX maturity assessment:
{responses}

Based on this data, please answer the following question: {question}

Keep your analysis focused on:
- UX maturity stages and progression
- Research methods and their effectiveness  
- Institutional characteristics and their impact
- Challenges and success factors in UX implementation
"""
        
        return ChatPromptTemplate.from_template(template)
'''
    
    with open(project_dir / "project.py", "w") as f:
        f.write(project_py_content)
    
    # Create prompt.txt
    prompt_content = """You are an expert in analyzing UX maturity and research methods in academic libraries.
Focus on providing insights about UX practices, maturity stages, and research methods used in university libraries.

Here is relevant data from the UX maturity assessment:
{responses}

Based on this data, please answer the following question: {question}

Keep your analysis focused on:
- UX maturity stages and progression
- Research methods and their effectiveness
- Institutional characteristics and their impact
- Challenges and success factors in UX implementation"""
    
    with open(project_dir / "prompt.txt", "w") as f:
        f.write(prompt_content)


def create_lcsh_project():
    """Create LCSH Variant Labels project files"""
    project_dir = Path("./projects/lcsh_variant_labels")
    
    # Create project.py
    project_py_content = '''"""
LCSH Variant Labels Project - Library of Congress Subject Headings variant analysis
"""
import pandas as pd
import os
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from base_project import BaseProject


class LCSHVariantProject(BaseProject):
    """LCSH Variant Labels project"""
    
    def process_row(self, row: pd.Series, index: int) -> Document:
        """Process LCSH variant labels row"""
        page_content = str(row['label_value'])
        return Document(page_content=page_content, id=str(index))
    
    def get_prompt_template(self) -> ChatPromptTemplate:
        """Load prompt template from file or use default"""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, 'r') as f:
                template = f.read()
        else:
            template = """
You are an expert in library cataloging and subject analysis.
Given a description, select the most relevant Library of Congress Subject Headings (LCSH) variant labels from the list below.

Candidate LCSH variant labels:
{responses}

Description: {question}

Return a list of the most relevant subject headings from the candidates above, and explain your reasoning.
You must only return subject headings from the list above. Do not invent or modify any headings. If none are relevant, return an empty list.
"""
        
        return ChatPromptTemplate.from_template(template)
    
    def get_batch_size(self) -> int:
        """Use larger batch size for LCSH data"""
        return 5000
'''
    
    with open(project_dir / "project.py", "w") as f:
        f.write(project_py_content)
    
    # Create prompt.txt
    prompt_content = """You are an expert in library cataloging and subject analysis.
Given a description, select the most relevant Library of Congress Subject Headings (LCSH) variant labels from the list below.

Candidate LCSH variant labels:
{responses}

Description: {question}

Return a list of the most relevant subject headings from the candidates above, and explain your reasoning.
You must only return subject headings from the list above. Do not invent or modify any headings. If none are relevant, return an empty list."""
    
    with open(project_dir / "prompt.txt", "w") as f:
        f.write(prompt_content)


def create_restaurant_reviews_project():
    """Create Restaurant Reviews project files if data exists"""
    project_dir = Path("./projects/restaurant_reviews")
    
    if not project_dir.exists():
        return
    
    # Create project.py
    project_py_content = '''"""
Restaurant Reviews Project - Analyzes restaurant reviews for sentiment and insights
"""
import pandas as pd
import os
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from base_project import BaseProject


class RestaurantReviewsProject(BaseProject):
    """Restaurant Reviews analysis project"""
    
    def process_row(self, row: pd.Series, index: int) -> Document:
        """Process restaurant review data row"""
        # Adjust these field names based on your CSV structure
        page_content = f"Restaurant: {row.get('restaurant_name', 'Unknown')} "
        if 'review_text' in row:
            page_content += f"Review: {row['review_text']} "
        if 'rating' in row:
            page_content += f"Rating: {row['rating']}"

        metadata = {
            "rating": row.get("rating", 0),
            "restaurant": row.get("restaurant_name", "Unknown")
        }
        
        return Document(page_content=page_content, metadata=metadata, id=str(index))
    
    def get_prompt_template(self) -> ChatPromptTemplate:
        """Load prompt template from file or use default"""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, 'r') as f:
                template = f.read()
        else:
            template = """
You are an expert in analyzing restaurant reviews and customer sentiment.
Focus on providing insights about customer experiences, service quality, and food satisfaction.

Here is relevant data from restaurant reviews:
{responses}

Based on this data, please answer the following question: {question}

Keep your analysis focused on:
- Customer satisfaction patterns
- Service quality indicators
- Food and dining experience insights
- Common themes in positive and negative feedback
"""
        
        return ChatPromptTemplate.from_template(template)
'''
    
    with open(project_dir / "project.py", "w") as f:
        f.write(project_py_content)
    
    # Create prompt.txt
    prompt_content = """You are an expert in analyzing restaurant reviews and customer sentiment.
Focus on providing insights about customer experiences, service quality, and food satisfaction.

Here is relevant data from restaurant reviews:
{responses}

Based on this data, please answer the following question: {question}

Keep your analysis focused on:
- Customer satisfaction patterns
- Service quality indicators
- Food and dining experience insights
- Common themes in positive and negative feedback"""
    
    with open(project_dir / "prompt.txt", "w") as f:
        f.write(prompt_content)


def main():
    """Create all project files"""
    print("Creating project-specific files...")
    
    if Path("./projects/ux_maturity").exists():
        create_ux_maturity_project()
        print("✓ Created UX Maturity project files")
    
    if Path("./projects/lcsh_variant_labels").exists():
        create_lcsh_project()
        print("✓ Created LCSH Variant Labels project files")
    
    if Path("./projects/restaurant_reviews").exists():
        create_restaurant_reviews_project()
        print("✓ Created Restaurant Reviews project files")
    
    print("\nAll project files created successfully!")
    print("You can now run: python3 new_main.py")


if __name__ == "__main__":
    main()
