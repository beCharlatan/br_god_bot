from config.database import db
from domain.models.documents_meta import DocumentMeta
from domain.models.ba_document_embedding import BADocumentEmbedding
from domain.models.sa_document_embedding import SADocumentEmbedding

if __name__ == "__main__":
    db.create_tables()
    print("Database tables created successfully")
