from domain.models.documents_meta import DocumentMeta
from scripts.base_document_loader import BaseDocumentLoader
from services.embeddings.ba_document_embedder import BADocumentEmbedder
from services.documents.ba_document_service import BADocumentService


class BADocumentLoader(BaseDocumentLoader):
    def get_document_service(self):
        return BADocumentService()

    def get_document_embedder(self):
        return BADocumentEmbedder()

    def create_or_update_document_meta(self, title: str, confluence_link: str) -> DocumentMeta:
        doc_meta = self.meta_service.get_document_by_title(title)
        if doc_meta:
            doc_meta.ba_document_confluence_link = confluence_link
            return doc_meta
        return self.meta_service.create_document_meta(title=title, ba_link=confluence_link)


if __name__ == '__main__':
    BADocumentLoader.run_cli()
