"""
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
        # Use the rich full_context for embedding
        page_content = str(row['full_context'])

        # Preserve all metadata for RAG context
        metadata = {
            "lcsh_id": str(row['id']),
            "authoritative_label": str(row['authoritative_label']),
            "variant_labels": str(row['variant_labels']),
            "broader_authorities": str(row['broader_authorities']),
            "narrower_authorities": str(row['narrower_authorities']),
            "related_authorities": str(row['related_authorities']),
            "classification": str(row['classification']),
            "marc_key": str(row['marc_key']),
            "sources_and_notes": str(row['sources_and_notes'])
        }
        # Clean up metadata - remove empty or 'nan' values
        metadata = {k: v for k, v in metadata.items() if v and v != 'nan' and v.strip()}

        return Document(page_content=page_content, metadata=metadata, id=str(index))
    
    def get_prompt_template(self) -> ChatPromptTemplate:
        """Load prompt template from file or use default"""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, 'r') as f:
                template = f.read()
        else:
            template = """
You are an expert research librarian specializing in Library of Congress Subject Headings (LCSH) and academic research strategy. 
Your role is to help university researchers optimize their literature searches by recommending the most effective subject headings.

## Context
The student is conducting academic research and needs guidance on which Library of Congress Subject Headings will yield the most comprehensive and relevant results in library catalogs, academic databases, and institutional repositories.

## Available Subject Headings with Metadata:
{responses}

## Student's Research Topic:
**Topic:** {question}

## Your Task:
Analyze the student's research topic and provide strategic subject heading recommendations using the enhanced metadata available to you.

### Primary Analysis:
1. **Identify Core Concepts**: Extract the main concepts, methodologies, disciplines, and scope from the student's topic
2. **Consider Research Level**: Assess whether this appears to be undergraduate, graduate, or advanced research
3. **Evaluate Interdisciplinary Aspects**: Identify if the topic spans multiple disciplines

### Recommendation Strategy:
**Provide 3 categories of subject headings:**

#### A) PRIMARY HEADINGS (2-4 headings)
- The most direct and specific headings that match the core topic
- These should be the student's starting point for comprehensive searches

#### B) BROADER/RELATED HEADINGS (1-3 headings)
- Broader conceptual headings that may contain relevant subtopics
- Related headings from connected disciplines or methodologies
- Use the hierarchical relationships (broader authorities) in the metadata

#### C) ALTERNATIVE/VARIANT APPROACHES (1-2 headings)
- Alternative terminology or approaches to the same concepts
- Headings that might capture different perspectives on the topic
- Use variant labels and related authorities from the metadata

### For Each Recommended Heading:
**Format:**
- **Heading**: [Exact LCSH heading]
- **ID**: [LCSH identifier if available]
- **Why relevant**: [2-3 sentences explaining the connection to the research topic]
- **Search strategy**: [Specific advice on how to use this heading effectively]
- **Related terms**: [Mention any variant terms or narrower concepts from metadata]

### Additional Guidance:
- **Cross-references**: If the metadata shows broader/narrower relationships, mention how the student might expand or narrow their search
- **Interdisciplinary note**: If relevant, explain how certain headings bridge disciplines
- **Database strategy**: Briefly note if certain headings work better in specific types of databases

### Quality Controls:
- Only recommend headings from the provided candidate list
- If no headings are sufficiently relevant, explain why and suggest the student refine their topic description
- Prioritize headings that will lead to peer-reviewed academic sources
- Consider both current terminology and historical subject heading evolution

### Output Format:
```
## RECOMMENDED SUBJECT HEADINGS

### PRIMARY HEADINGS
[List with explanations]

### BROADER/RELATED HEADINGS  
[List with explanations]

### ALTERNATIVE/VARIANT APPROACHES
[List with explanations]

## SEARCH STRATEGY NOTES
[Any additional strategic advice for using these headings effectively]
```

Remember: Your goal is not just to match keywords, but to leverage the rich hierarchical and relational structure 
of LCSH to guide the researcher toward the most productive search strategies for their specific academic inquiry.

You must only return subject headings from the list above. Do not invent or modify any headings. 
If none are relevant, return an empty list.
"""
        
        return ChatPromptTemplate.from_template(template)
    
    def get_batch_size(self) -> int:
        """Use larger batch size for LCSH data"""
        return 5000
