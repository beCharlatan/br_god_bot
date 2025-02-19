from abc import ABC, abstractmethod
import argparse
from typing import Optional

from domain.models.documents_meta import DocumentMeta
from services.preprocessing.preprocessor import Preprocessor
from services.documents.document_meta_service import DocumentMetaService


class BaseDocumentLoader(ABC):
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.meta_service = DocumentMetaService()

    @abstractmethod
    def get_document_service(self):
        pass

    @abstractmethod
    def get_document_embedder(self):
        pass

    @abstractmethod
    def create_or_update_document_meta(self, title: str, confluence_link: str) -> DocumentMeta:
        pass

    def load_document(self, file_path: str, confluence_link: str):
        # Validate and preprocess the document
        self.preprocessor.validate_file(file_path)
        title, content = self.preprocessor.extract_text_from_docx(file_path)

        # Get or create document metadata
        doc_meta = self.create_or_update_document_meta(title, confluence_link)

        # Process document and create embeddings
        # process_document метод уже сохраняет чанки в базу через store_document_embedding
        embedder = self.get_document_embedder()
        embedder.process_document(content, doc_meta.id)

    @classmethod
    def run_cli(cls):
        parser = argparse.ArgumentParser(description='Load document into vector storage')
        parser.add_argument('file_path', help='Path to the DOCX file')
        parser.add_argument('confluence_link', help='Link to the Confluence page')
        
        args = parser.parse_args()
        loader = cls()
        loader.load_document(args.file_path, args.confluence_link)
