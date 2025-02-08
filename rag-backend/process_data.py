from PyPDF2 import PdfReader
from knowledge_graph import KnowledgeGraphBuilder
import re
from typing import List, Tuple

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using pdf."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def clean_text_content(text: str) -> str:
    """Clean and normalize text."""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep periods and commas
    text = re.sub(r'[^a-zA-Z0-9\s.,]', '', text)
    return text.strip()

def split_into_chunks(text: str, chunk_size: int = 1000) -> List[str]:
    """Split text into chunks of approximately equal size."""
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def process_pdf(file_path: str) -> Tuple[str, KnowledgeGraphBuilder]:
    """Process PDF and build knowledge graph."""
    # Extract text
    text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text_content(text)
    
    # Build knowledge graph
    kg_builder = KnowledgeGraphBuilder()
    kg_builder.build_graph(cleaned_text)
    
    return cleaned_text, kg_builder

def generate_enhanced_context(query: str, text: str, kg_builder: KnowledgeGraphBuilder) -> str:
    """Generate context using both text chunks and knowledge graph."""
    # Get relevant paths from knowledge graph
    kg_context = kg_builder.query_graph(query)
    
    # Get relevant text chunks
    chunks = split_into_chunks(text)
    relevant_chunks = [chunk for chunk in chunks if any(term in chunk.lower() for term in query.lower().split())]
    
    # Combine both sources with clear separation
    context_parts = []
    
    if kg_context:
        context_parts.append(f"Knowledge Graph Relationships:\n{kg_context}")
    
    if relevant_chunks:
        context_parts.append(f"Relevant Text:\n{' '.join(relevant_chunks[:2])}")
    
    if not context_parts:
        return "No relevant information found in the document."
        
    return "\n\n".join(context_parts)

