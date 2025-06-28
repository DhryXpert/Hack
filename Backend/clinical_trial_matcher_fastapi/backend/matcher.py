from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TrialMatcher:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.trial_embeddings = None
        self.trials_df = None

    def load_trials(self, trials_df):
        self.trials_df = trials_df
        trial_texts = []
        for _, trial in trials_df.iterrows():
            text = f"{trial['title']} {' '.join(trial['condition'])} {trial['eligibility']}"
            trial_texts.append(text)
        self.trial_embeddings = self.model.encode(trial_texts)

    def match_patient(self, patient_profile, top_k=5):
        patient_text = f"""
        Age: {patient_profile['age']}
        Gender: {patient_profile['gender']}
        Conditions: {' '.join(patient_profile['conditions'])}
        Symptoms: {' '.join(patient_profile['symptoms'])}
        Location: {patient_profile['location']}
        """
        patient_embedding = self.model.encode([patient_text])
        similarities = cosine_similarity(patient_embedding, self.trial_embeddings)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        matches = []
        for idx in top_indices:
            match = {
                'trial': self.trials_df.iloc[idx].to_dict(),
                'similarity_score': similarities[idx],
                'match_reasons': self._get_match_reasons(patient_profile, self.trials_df.iloc[idx])
            }
            matches.append(match)
        return matches

    def _get_match_reasons(self, patient, trial):
        reasons = []
        patient_conditions = [c.lower() for c in patient['conditions']]
        trial_conditions = [c.lower() for c in trial['condition']]
        common_conditions = set(patient_conditions) & set(trial_conditions)
        if common_conditions:
            reasons.append(f"Matching conditions: {', '.join(common_conditions)}")
        return reasons
