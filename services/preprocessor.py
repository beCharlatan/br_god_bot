import argparse
from pathlib import Path
from docx import Document
from typing import List, Tuple
from config.database import db
from domain.models.document_image import DocumentImage
from domain.models.file_embeddings import FileEmbeddings
from services.document_files_store import DocumentFilesStore

class Preprocessor:
    def parse_arguments(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Генерация тест-кейсов по бизнес-требованниям')
        parser.add_argument('input_file', type=str, help='Path to DOCX file with business requirements')
        return parser.parse_args()
    
    def validate_file(self, file_path: str) -> None:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if path.suffix.lower() != '.docx':
            raise ValueError(f"Invalid file type. Expected .docx file, got: {path.suffix}")
    
    def extract_text_from_docx(self, file_path: str) -> str:
        try:
            doc = Document(file_path)
            paragraphs = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    paragraphs.append(paragraph.text)
            
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            paragraphs.append(cell.text)
            
            return "\n\n".join(paragraphs)
        except Exception as e:
            raise ValueError(f"Error reading docx file: {str(e)}")
    
    def extract_images_from_docx(self, file_path: str) -> List[Tuple[str, bytes]]:
        """Extract all images from a DOCX file"""
        doc = Document(file_path)
        images = []
        
        # Process images from shapes in the document
        for rel in doc.part.rels.values():
            if "image" in rel.reltype:
                image_data = rel.target_part.blob
                image_name = rel.target_part.partname.split('/')[-1]
                images.append((image_name, image_data))
        
        return images

    def process_document_images(self, file_path: str) -> List[str]:
        """Extract images from DOCX and store them in MinIO"""
        self.validate_file(file_path)
        
        # Initialize services
        files_store = DocumentFilesStore()
        
        try:
            # Extract images
            images = self.extract_images_from_docx(file_path)
            stored_urls = []
            
            with next(db.get_db()) as session:
                # Get or create FileEmbeddings entry
                file_embedding = session.query(FileEmbeddings).filter_by(original_filename=file_path).first()
                if not file_embedding:
                    file_embedding = FileEmbeddings(original_filename=file_path)
                    session.add(file_embedding)
                    session.flush()
                
                # Store each image
                for image_name, image_data in images:
                    # Upload to MinIO
                    minio_path = files_store.upload_image(image_data, image_name)
                    if minio_path:
                        # Get the URL
                        url = files_store.get_image_url(minio_path)
                        stored_urls.append(url)
                        
                        # Store in database
                        doc_image = DocumentImage(
                            image_name=image_name,
                            minio_path=minio_path,
                            file_embedding_id=file_embedding.id
                        )
                        session.add(doc_image)
                
                # Commit all database changes
                session.commit()
                return stored_urls
            
        except Exception as e:
            raise ValueError(f"Error processing document images: {str(e)}")

    def read_requirements_file(self, file_path: str) -> str:
        self.validate_file(file_path)
        content = self.extract_text_from_docx(file_path)
        self.process_document_images(file_path)
        
        return content
