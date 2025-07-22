"""
Subject Guides Project - Library Subject Guides RAG vector store creation
Refactored for CSV data structure from subject_guides_2_truncated.csv
"""
import pandas as pd
import os
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from base_project import BaseProject


class SubjectGuidesProject(BaseProject):
    """Subject Guides project for creating RAG vector store from CSV data"""

    def process_row(self, row: pd.Series, index: int) -> Document:
        """Process subject guides row to create rich context for RAG"""

        # Map CSV columns based on the structure we observed
        # Column 0: subject_id (60860)
        # Column 1: subject_title ("2014 US-Cuba Policy Research Guide")
        # Column 2: subject_shortform ("cubapolicy2014") - used for URL
        # Column 3: subject_description
        # Column 6: tab_name ("Main")
        # Column 7: section_title
        # Column 8: section_content
        # Column 10: staff_id
        # Column 11: staff_lastname
        # Column 12: staff_firstname
        # Column 13: staff_email
        # Column 14: staff_title
        # Column 15: staff_phone
        # Column 16: staff_fullname
        # Column 17: department_id
        # Column 18: department_name

        # Create comprehensive page content by combining key fields
        content_parts = []

        # Add subject information
        subject_title = self._get_column_value(row, 1, "")
        subject_shortform = self._get_column_value(row, 2, "")
        subject_description = self._get_column_value(row, 3, "")
        tab_name = self._get_column_value(row, 6, "")
        section_title = self._get_column_value(row, 7, "")
        section_content = self._get_column_value(row, 8, "")

        # Staff information
        staff_firstname = self._get_column_value(row, 12, "")
        staff_lastname = self._get_column_value(row, 11, "")
        staff_email = self._get_column_value(row, 13, "")
        staff_title = self._get_column_value(row, 14, "")
        staff_phone = self._get_column_value(row, 15, "")
        department_name = self._get_column_value(row, 18, "")

        # Build content for embedding
        if subject_title:
            content_parts.append(f"Subject Guide: {subject_title}")

        if subject_description:
            content_parts.append(f"Description: {subject_description}")

        if tab_name:
            content_parts.append(f"Tab: {tab_name}")

        if section_title:
            content_parts.append(f"Section: {section_title}")

        # Add staff information
        if staff_firstname and staff_lastname:
            staff_name = f"{staff_firstname} {staff_lastname}"
            content_parts.append(f"Subject Librarian: {staff_name}")

        if staff_email:
            content_parts.append(f"Librarian Email: {staff_email}")

        if department_name:
            content_parts.append(f"Department: {department_name}")

        # Add section content (truncate if very long)
        if section_content:
            clean_content = self._clean_html_content(section_content)
            if len(clean_content) > 2000:
                clean_content = clean_content[:2000] + "..."
            content_parts.append(f"Content: {clean_content}")

        # Join all parts with newlines for rich context
        page_content = "\n\n".join(content_parts)

        # If no meaningful content, create a basic description
        if not page_content.strip():
            page_content = f"Subject Guide Entry {index}"

        # Preserve metadata for RAG context
        metadata = {}

        # Core identification
        subject_id = self._get_column_value(row, 0, "")
        if subject_id:
            metadata['subject_id'] = str(subject_id)

        if subject_title:
            metadata['subject_title'] = str(subject_title)

        if subject_shortform:
            metadata['subject_shortform'] = str(subject_shortform)
            # Create guide URL
            metadata['guide_url'] = f"https://guides.library.miami.edu/{subject_shortform}"

        if subject_description:
            metadata['subject_description'] = str(subject_description)

        # Tab and section info
        if tab_name:
            metadata['tab_name'] = str(tab_name)

        if section_title:
            metadata['section_title'] = str(section_title)

        # Staff information for contact
        if staff_firstname:
            metadata['staff_firstname'] = str(staff_firstname)
        if staff_lastname:
            metadata['staff_lastname'] = str(staff_lastname)
        if staff_email:
            metadata['staff_email'] = str(staff_email)
            # Create formatted staff contact
            if staff_firstname and staff_lastname:
                staff_contact = f"{staff_firstname} {staff_lastname}, <a href=\"mailto:{staff_email}\">{staff_email}</a>"
                metadata['staff_contact_html'] = staff_contact
        if staff_title:
            metadata['staff_title'] = str(staff_title)
        if staff_phone:
            metadata['staff_phone'] = str(staff_phone)
        if department_name:
            metadata['department_name'] = str(department_name)

        # Additional IDs
        staff_id = self._get_column_value(row, 10, "")
        department_id = self._get_column_value(row, 17, "")
        if staff_id:
            metadata['staff_id'] = str(staff_id)
        if department_id:
            metadata['department_id'] = str(department_id)

        return Document(page_content=page_content, metadata=metadata, id=str(index))

    def _get_column_value(self, row: pd.Series, column_index: int, default=""):
        """Safely get column value by index"""
        try:
            if len(row) > column_index:
                value = row.iloc[column_index]
                if pd.notna(value) and str(value).strip():
                    return str(value).strip()
        except:
            pass
        return default

    def _clean_html_content(self, content: str) -> str:
        """Clean HTML content for better readability"""
        import re

        # Remove HTML tags but keep text content
        content = re.sub(r'<[^>]+>', ' ', content)

        # Replace HTML entities
        content = content.replace('&amp;', '&')
        content = content.replace('&lt;', '<')
        content = content.replace('&gt;', '>')
        content = content.replace('&quot;', '"')
        content = content.replace('&#39;', "'")
        content = content.replace('&nbsp;', ' ')

        # Clean up whitespace
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()

        return content

    def get_prompt_template(self) -> ChatPromptTemplate:
        """Load prompt template from file or use default"""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, 'r') as f:
                template = f.read()
        else:
            template = """
You are an expert research librarian and subject guide specialist. Your role is to help students, faculty, and researchers 
find the most relevant and comprehensive library subject guides for their academic and research needs.

## Context
The user is seeking library resources and research guidance for their specific topic or course. You have access to a 
comprehensive database of library subject guides, each containing curated resources, research strategies, and expert guidance.

## Available Subject Guides:
{responses}

## User's Request:
**Topic/Course/Research Area:** {question}

## Your Task:
Analyze the user's request and recommend the most relevant subject guides that will best support their research and learning objectives.

### CRITICAL REQUIREMENTS:
- **ONLY recommend guides that appear in the "Available Subject Guides" section above**
- **NEVER create, invent, or modify any guide information**
- **ALL URLs must use the exact shortform from the metadata, converted to lowercase**
- **If no guides are sufficiently relevant, say so explicitly and suggest alternatives**

### Analysis Framework:
1. **Topic Matching**: Identify guides that directly address the user's subject area
2. **Course Alignment**: Match course codes, instructor names, or academic level when provided
3. **Research Scope**: Consider whether the user needs broad introductory resources or specialized research materials
4. **Interdisciplinary Connections**: Identify guides from related fields that might offer valuable perspectives

### Recommendation Categories:

#### A) PRIMARY GUIDES (1-3 guides)
The most directly relevant guides for the user's specific topic or course
- Should be the user's first stop for comprehensive resources
- Focus on exact subject matches and course-specific guides

#### B) SUPPLEMENTARY GUIDES (1-2 guides)
Additional guides that provide broader context or complementary perspectives
- Related disciplines that inform the main topic
- Methodological or theoretical frameworks relevant to the research

#### C) SPECIALIZED RESOURCES (0-2 guides)
Highly focused guides for specific aspects of the topic
- Advanced research methodologies
- Specialized databases or collections
- Historical or theoretical perspectives

### For Each Recommended Guide:
**MANDATORY FORMAT - Use EXACT information from the provided guides:**
- **Guide Title**: [Use the EXACT subject_title from the guide metadata]
- **Guide URL**: https://guides.library.miami.edu/[shortform from metadata, converted to lowercase]
- **Subject Librarian**: [Use EXACT staff name and email from metadata, format as: Name, <a href="mailto:email">email</a>]
- **Department**: [Use EXACT department_name from metadata]
- **Relevance**: [2-3 sentences explaining why this guide matches the user's needs]
- **Key Resources**: [Brief description based ONLY on the actual content provided]
- **Best Use**: [When and how the user should consult this guide]

### URL Construction Rules:
- Take the shortform from the guide's metadata
- Convert the shortform to lowercase
- Format as: https://guides.library.miami.edu/[lowercase_shortform]
- Example: If shortform is "CubaPolicy2014", the URL becomes https://guides.library.miami.edu/cubapolicy2014

### Quality Controls:
- **VERIFICATION REQUIRED**: Before recommending any guide, verify it exists in the "Available Subject Guides" section
- **NO HALLUCINATIONS**: Never create guides that don't exist in the provided data
- **EXACT METADATA**: Use only the exact titles, names, emails, and shortforms from the provided guide metadata
- **URL ACCURACY**: Always convert shortform to lowercase for URLs
- If uncertain about any guide details, omit that guide rather than guess

### When No Relevant Guides Exist:
If no guides in the provided database are sufficiently relevant:
```
## NO DIRECTLY RELEVANT GUIDES FOUND

Based on my analysis of the available subject guides database, I could not find guides that directly match your research topic of "[topic]".

### SUGGESTIONS:
1. **Contact General Reference**: For assistance finding resources outside our subject guide collection
2. **Try Related Keywords**: Consider broader or related terms that might match available guides
3. **Subject Librarian Consultation**: Contact a subject librarian in a related field for personalized assistance

### CLOSEST AVAILABLE GUIDES:
[Only list if there are tangentially related guides with clear explanations of why they're not perfect matches]
```

### Output Format:
```
## RECOMMENDED SUBJECT GUIDES

### PRIMARY GUIDES
**[Exact Guide Title from Metadata]**
- **URL**: https://guides.library.miami.edu/[lowercase_shortform]
- **Subject Librarian**: [Exact Name], <a href="mailto:[exact_email]">[exact_email]</a>
- **Department**: [Exact Department Name]
- **Relevance**: [Explanation based on actual guide content]
- **Key Resources**: [Description based on actual provided content]
- **Best Use**: [Usage guidance]

### SUPPLEMENTARY GUIDES
[Same format as above, only if applicable]

### SPECIALIZED RESOURCES
[Same format as above, only if applicable]

## RESEARCH STRATEGY
[Guidance on how to use these guides effectively together]

## CONTACT FOR ADDITIONAL HELP
[List primary subject librarian contacts for follow-up questions]
```

### Final Verification Checklist:
Before providing your response, verify:
- [ ] All recommended guides appear in the provided database
- [ ] All URLs use lowercase shortforms
- [ ] All librarian names and emails are exactly as provided in metadata
- [ ] All guide titles are exactly as provided in metadata
- [ ] No information has been invented or modified

Remember: Accuracy is more important than completeness. It's better to recommend fewer guides with perfect accuracy than to include any invented or modified information. Your credibility as a librarian depends on providing only verified, accurate information from the actual database.
"""

        return ChatPromptTemplate.from_template(template)

    def get_batch_size(self) -> int:
        """Use appropriate batch size for subject guide data"""
        return 1000

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the CSV data before creating documents"""
        # Remove completely empty rows
        df = df.dropna(how='all')

        # The CSV doesn't have proper headers, so we'll work with positional columns
        # Ensure we have enough columns (the CSV has 303 columns)
        expected_columns = 303
        if df.shape[1] < expected_columns:
            # Add missing columns filled with empty strings
            for i in range(df.shape[1], expected_columns):
                df[f'col_{i}'] = ""

        # Remove duplicate entries based on subject_id, tab, and section
        # This helps reduce redundant content while keeping unique sections
        duplicate_cols = [0, 6, 7]  # subject_id, tab_name, section_title
        df = df.drop_duplicates(subset=duplicate_cols, keep='first')

        return df

    def get_collection_name(self) -> str:
        """Return the collection name for this project"""
        return "subject_guides"

    def get_description(self) -> str:
        """Return a description of this project"""
        return "Library Subject Guides RAG vector store for research assistance and resource discovery with complete URLs and librarian contact information"