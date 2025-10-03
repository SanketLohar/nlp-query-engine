# backend/services/document_processor.py

import os
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import docx
import pypdf

class DocumentProcessor:
    def __init__(self, doc_folder_path: str = "documents"):
        self.doc_folder_path = doc_folder_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.chunks = []
        self._build_index()

    def _extract_text(self, file_path):
        """Extracts text from PDF, DOCX, or TXT files."""
        text = ""
        if file_path.endswith(".pdf"):
            with open(file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text()
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding='utf-8') as f:
                text = f.read()
        return text

    def _build_index(self):
        """Builds the FAISS index from documents in the specified folder."""
        filepaths = [os.path.join(self.doc_folder_path, f) for f in os.listdir(self.doc_folder_path)]
        
        all_texts = []
        for path in filepaths:
            # Simple chunking: split by paragraph
            doc_text = self._extract_text(path)
            paragraphs = doc_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    self.chunks.append({'source': os.path.basename(path), 'content': para.strip()})
        
        if not self.chunks:
            return

        # Generate embeddings
        contents = [chunk['content'] for chunk in self.chunks]
        embeddings = self.model.encode(contents, convert_to_tensor=False)
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings, dtype=np.float32))
        print(f"✅ Document index built successfully with {len(self.chunks)} chunks.")

    def search(self, query: str, k: int = 3):
        """Searches the document index for a given query."""
        if self.index is None or len(self.chunks) == 0:
            return []
        
        query_embedding = self.model.encode([query], convert_to_tensor=False)
        distances, indices = self.index.search(np.array(query_embedding, dtype=np.float32), k)
        
        results = []
        for i in indices[0]:
            if i < len(self.chunks):
                results.append(self.chunks[i])
        return results