# Multi-Project RAG System - User Guide

## Overview

The LocalAIAgentWithRAG has been enhanced to support multiple projects with different data types and specialized prompts. Each project is self-contained with its own data, processing logic, and prompt templates.

## Architecture

### Project Structure
```
projects/
├── ux_maturity/
│   ├── data.csv          # UX maturity research data
│   ├── project.py        # Processing logic for UX data
│   └── prompt.txt        # Specialized prompt for UX analysis
├── lcsh_variant_labels/
│   ├── data.csv          # Library of Congress Subject Headings
│   ├── project.py        # Processing logic for LCSH data
│   └── prompt.txt        # Specialized prompt for cataloging
└── restaurant_reviews/
    ├── data.csv          # Restaurant review data
    ├── project.py        # Processing logic for reviews
    └── prompt.txt        # Specialized prompt for sentiment analysis
```

### Core Components

- **BaseProject**: Abstract base class defining common functionality
- **ProjectManager**: Discovers and manages multiple projects
- **Project-specific classes**: Custom implementations for each data type

## Usage

### Interactive Mode

1. Activate the virtual environment:
```bash
source venv/bin/activate
```

2. Run the multi-project application:
```bash
python3 new_main.py
```

3. Available commands:
- `list` - Show available projects
- `select <project_name>` - Select a project to work with
- `refresh` - Refresh all vector stores
- `q` - Quit

### Example Session

```
Multi-Project RAG System
Commands:
  list - List available projects
  select <project_name> - Select a project
  refresh - Refresh all vector stores
  q - Quit

Enter command or select a project first: list
Available projects: lcsh_variant_labels, restaurant_reviews, ux_maturity

Enter command or select a project first: select ux_maturity
Selected project: ux_maturity

[ux_maturity] Ask your question (or command): What factors influence UX maturity in academic libraries?
```

## Available Projects

### 1. UX Maturity (`ux_maturity`)
- **Data**: Academic library UX research maturity assessment
- **Use case**: Analyze UX practices, maturity stages, and research methods
- **Sample questions**:
  - "What are the key factors that influence UX maturity?"
  - "Which research methods are most effective?"
  - "How do institutional characteristics impact UX implementation?"

### 2. LCSH Variant Labels (`lcsh_variant_labels`)
- **Data**: Library of Congress Subject Headings variant labels
- **Use case**: Subject cataloging and classification assistance
- **Sample questions**:
  - "library automation systems"
  - "artificial intelligence in education"
  - "digital preservation methods"

### 3. Restaurant Reviews (`restaurant_reviews`)
- **Data**: Customer restaurant reviews and ratings
- **Use case**: Sentiment analysis and customer experience insights
- **Sample questions**:
  - "What do customers say about service quality?"
  - "Which restaurants have the best food ratings?"
  - "What are common complaints in negative reviews?"

## Adding New Projects

### 1. Create Project Directory
```bash
mkdir projects/my_new_project
```

### 2. Add Required Files

**data.csv**: Your dataset in CSV format

**prompt.txt**: Custom prompt template
```
You are an expert in [your domain].
Given the following data: {responses}
Please answer this question: {question}
Focus your analysis on: [specific aspects]
```

**project.py**: Processing logic
```python
import pandas as pd
import os
import sys
from pathlib import Path
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

sys.path.append(str(Path(__file__).parent.parent.parent))
from base_project import BaseProject

class MyNewProject(BaseProject):
    def process_row(self, row: pd.Series, index: int) -> Document:
        # Custom processing logic for your data
        page_content = f"Your content: {row['your_column']}"
        metadata = {"your_field": row.get("your_field", "")}
        return Document(page_content=page_content, metadata=metadata, id=str(index))
    
    def get_prompt_template(self) -> ChatPromptTemplate:
        with open(self.prompt_file, 'r') as f:
            template = f.read()
        return ChatPromptTemplate.from_template(template)
```

### 3. Initialize the New Project
```bash
source venv/bin/activate
python3 -c "from project_manager import ProjectManager; pm = ProjectManager(); pm.initialize_all_projects(force_refresh=True)"
```

## Legacy Support

The original single-project application is still available:
```bash
python3 main.py
```

## Testing

Run the comprehensive test suite:
```bash
source venv/bin/activate
python3 quick_test.py
```

## Troubleshooting

### Project Not Found
- Ensure all required files (data.csv, project.py, prompt.txt) exist
- Check that the project class inherits from BaseProject
- Verify CSV file has the expected column names

### Import Errors
- Make sure the virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Vector Store Issues
- Refresh vector stores: Use the `refresh` command in interactive mode
- Or manually: `python3 -c "from project_manager import ProjectManager; pm = ProjectManager(); pm.initialize_all_projects(force_refresh=True)"`

## Performance Notes

- Initial vector store creation may take time for large datasets
- Subsequent runs use cached vector stores for faster startup
- LCSH project uses larger batch sizes (5000) for efficiency
- Other projects use standard batch sizes (1000)

## Next Steps

- Add more specialized projects for different domains
- Implement custom evaluation metrics per project
- Add support for different embedding models per project
- Create project templates for common use cases
