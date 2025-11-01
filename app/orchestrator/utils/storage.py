import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.config import settings

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(path=settings.VECTOR_DB_PATH)
        self.collection = settings.COLLECTION_NAME
        if self.collection not in [c.name for c in self.client.get_collections().collections]:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

    def add_documents(self, vectors, metadatas):
        points = [
            PointStruct(id=i, vector=vectors[i].tolist(), payload=metadatas[i])
            for i in range(len(vectors))
        ]
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, query_vector, limit=5):
        return self.client.search(collection_name=self.collection, query_vector=query_vector, limit=limit)