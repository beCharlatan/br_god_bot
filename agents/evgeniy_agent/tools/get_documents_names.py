from langchain.tools import tool
from services.documents.document_meta_service import DocumentMetaService
from typing import List


@tool
def get_documents_names() -> List[tuple[str, str | None, str | None]]:
    """
    Инструмент для получения метаданных всех документов в базе знаний продукта.
    
    Этот инструмент интегрируется с хранилищем документов и извлекает
    метаданные всех документов, доступных для поиска и анализа. Он полезен для
    определения доступных источников информации, их расположения в Confluence
    и проверки покрытия требований.

    Параметры:
        Нет входных параметров. Инструмент автоматически обращается к
        хранилищу документов для получения данных.

    Возвращает:
        List[tuple[str, str | None, str | None]]: Список кортежей, где каждый кортеж содержит:
            - str: Название документа
            - str | None: Ссылка на документ бизнес-анализа в Confluence (или None)
            - str | None: Ссылка на документ системного анализа в Confluence (или None)

    Использование:
        1. Определение всех доступных документов для поиска информации.
        2. Получение ссылок на документы в Confluence для перехода к первоисточнику.
        3. Определение связей между бизнес и системными требованиями.
        4. Генерация содержимого на основе требований.

    Примеры использования:
        >>> get_documents_names()
        [('Красная кнопка', 'https://confluence.../br-doc', None),
         ('Архитектура системы', None, 'https://confluence.../sa-doc')]

    Ограничения:
        - Возвращает только метаданные документов, а не их содержимое.
        - Требует корректной настройки связей между документами в базе данных.
        - Зависит от доступности и актуальности данных в хранилище.
    """

    # Log agent tool activation
    print(f'[BR Agent] Fetching all business requirements')

    # Access document storage service
    document_meta_service = DocumentMetaService()
    return [(doc.title, doc.ba_document_confluence_link, doc.sa_document_confluence_link) for doc in document_meta_service.get_all_documents()]