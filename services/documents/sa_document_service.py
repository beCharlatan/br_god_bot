from typing import List, Dict
from domain.models.sa_document_embedding import SADocumentEmbedding
from services.documents.base_document_service import BaseDocumentService

class SADocumentService(BaseDocumentService[SADocumentEmbedding]):
    def __init__(self):
        super().__init__(SADocumentEmbedding)
    
    def store_document_embedding(self, content: str, embedding: List[float], document_meta_id: int) -> None:
        """Store SA document embedding."""
        with self._get_session() as session:
            doc_embedding = SADocumentEmbedding(
                content=content,
                embedding=str(embedding),
                document_meta_id=document_meta_id
            )
            session.add(doc_embedding)
            session.commit()
    
    def find_similar_documents(self, query_embedding: List[float], query_text: str, 
                             bi_encoder_limit: int = 10, final_limit: int = 3) -> List[Dict]:
        """Find similar SA documents using two-stage retrieval."""
        bi_encoder_results = []
        
        try:
            with self._get_session() as session:
                # Join с таблицей метаданных для получения ссылки на confluence
                documents = session.query(self.model_class, 'documents_meta.sa_document_confluence_link').\
                    join('document_meta').all()
                if not documents:
                    print("Warning: No SA documents found in the database")
                    return []

                for doc, confluence_link in documents:
                    try:
                        stored_embedding = self._parse_embedding(doc.embedding)
                        if len(stored_embedding) != len(query_embedding):
                            print(f"Warning: Skipping document due to embedding dimension mismatch")
                            continue

                        similarity = self._calculate_similarity(query_embedding, stored_embedding)
                        bi_encoder_results.append({
                            'content': doc.content,
                            'similarity': similarity,
                            'confluence_link': confluence_link
                        })
                    except Exception as e:
                        print(f"Error processing document: {str(e)}")
                        continue

            if not bi_encoder_results:
                print("No valid results found in bi-encoder stage")
                return []

            # Get top-k results from bi-encoder
            bi_encoder_results.sort(key=lambda x: x['similarity'], reverse=True)
            top_candidates = bi_encoder_results[:bi_encoder_limit]

            try:
                # Cross-encoder reranking
                cross_encoder_inputs = [(query_text, doc['content']) for doc in top_candidates]
                cross_scores = self.cross_encoder.predict(cross_encoder_inputs)

                # Combine results with cross-encoder scores
                for idx, score in enumerate(cross_scores):
                    top_candidates[idx]['cross_encoder_score'] = float(score)

                # Sort by cross-encoder scores and return top results
                final_results = sorted(top_candidates, key=lambda x: x['cross_encoder_score'], reverse=True)
                return final_results[:final_limit]

            except Exception as e:
                print(f"Error during cross-encoder reranking: {str(e)}")
                return top_candidates[:final_limit]

        except Exception as e:
            print(f"Error in find_similar_documents: {str(e)}")
            return []
