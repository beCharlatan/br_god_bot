from langchain.tools import tool
from services.document_embedder import DocumentEmbedder
from typing import List, Dict


@tool
def find_related_docs(query: str) -> List[Dict]:
  """Возвращает релевантную информацию о ближайших документах по запросу"""

  print(f'bot requested find_related_docs with query {query}')

  document_embedder = DocumentEmbedder()
  return document_embedder.find_similar_documents(query, limit=3)