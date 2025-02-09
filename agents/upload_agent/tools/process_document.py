from langchain_core.tools import Tool
from services.preprocessor import Preprocessor
from services.document_embedder import DocumentEmbedder

def _process_document(file_path: str) -> str:
    """
    Функция получает путь до файла и парсит документ с требованиями бизнеса.

    Args:
        file_path (str): Абсолютный путь до файла

    Returns:
        str: Текст документа.
    """
    print(f'bot requested process_document with file_path {file_path}')
    preprocessor = Preprocessor()
    document_embedder = DocumentEmbedder()
    content = preprocessor.read_requirements_file(file_path)
    return document_embedder.process_document(file_path, content)

process_document = Tool(
    name="process_document",
    description="Process and parse a business requirements document",
    func=_process_document
)