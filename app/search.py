from sentence_transformers import SentenceTransformer, util
import numpy as np

class SearchEngine:
    def __init__(self, apps_df):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.apps_df = apps_df
        self.app_names = apps_df['App'].tolist()
        self.embeddings = self.model.encode(self.app_names, convert_to_tensor=True)
    
    def suggest(self, query, top_k=5):
        if len(query) < 3:
            return []
        query_embedding = self.model.encode([query], convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0].cpu().numpy()
        top_indices = np.argsort(scores)[::-1][:top_k]
        suggestions = [self.app_names[i] for i in top_indices]
        return suggestions

    def search(self, query, top_k=10):
        query_embedding = self.model.encode([query], convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0].cpu().numpy()
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = self.apps_df.iloc[top_indices]
        return results