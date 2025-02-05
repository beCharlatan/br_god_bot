from langchain.tools import tool
from services.document_store import DocumentStore

@tool
def get_document_content(filename: str) -> str:
    """
    Возвращает текстовый контент документа по его наименованию.

    Args:
        filename (str): Название файла, для которого требуется получить контент

    Returns:
        str: Конкатенированный текст всех документов, связанных с указанным файлом

    Пример использования:
        >>> content = get_document_content("example.txt")
        >>> print(content)
        "Текст документа 1 Текст документа 2 Текст документа 3"

    Примечания:
        - Использует DocumentStore для получения данных
        - Конкатенация выполняется через пробел по умолчанию
        - Если документы не найдены, возвращает пустую строку
    """
    document_store = DocumentStore()

    file_id = document_store.get_document_id_by_name(filename)
    
    return document_store.get_concatenated_embeddings(file_id)