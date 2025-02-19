from domain.models.documents_meta import DocumentMeta
from scripts.base_document_loader import BaseDocumentLoader
from services.embeddings.sa_document_embedder import SADocumentEmbedder
from services.documents.sa_document_service import SADocumentService


class SADocumentLoader(BaseDocumentLoader):
    def get_document_service(self):
        return SADocumentService()

    def get_document_embedder(self):
        return SADocumentEmbedder()

    def create_or_update_document_meta(self, title: str, confluence_link: str) -> DocumentMeta:
        doc_meta = self.meta_service.get_document_by_title(title)
        if doc_meta:
            doc_meta.sa_document_confluence_link = confluence_link
            return doc_meta
        return self.meta_service.create_document_meta(title=title, sa_link=confluence_link)


if __name__ == '__main__':
    SADocumentLoader.run_cli()
