from typing import List, Optional
from domain.models.documents_meta import DocumentMeta
from services.documents.base_document_service import BaseDocumentService

class DocumentMetaService(BaseDocumentService[DocumentMeta]):
    def __init__(self):
        super().__init__(DocumentMeta)
    
    def create_document_meta(self, title: str, ba_link: Optional[str] = None, sa_link: Optional[str] = None) -> DocumentMeta:
        """Create a new document metadata entry."""
        session = self._get_session()
        doc_meta = DocumentMeta(
            title=title,
            ba_document_confluence_link=ba_link,
            sa_document_confluence_link=sa_link
        )
        session.add(doc_meta)
        session.commit()
        return doc_meta
    
    def get_all_documents(self) -> List[DocumentMeta]:
        """Get all document metadata entries."""
        try:
            with self._get_session() as session:
                return session.query(self.model_class).all()
        except Exception as e:
            print(f"Error fetching documents: {str(e)}")
            return []
    
    def get_document_by_title(self, title: str) -> Optional[DocumentMeta]:
        """Get document metadata by title."""
        try:
            with self._get_session() as session:
                return session.query(self.model_class).filter_by(title=title).first()
        except Exception as e:
            print(f"Error fetching document by title: {str(e)}")
            return None
