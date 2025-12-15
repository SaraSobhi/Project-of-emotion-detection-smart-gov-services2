import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
from utils import clean_text, has_negation, add_negation_feature

class ModelWrapper:
    def __init__(self, model_path="my_gov_model"):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        if not os.path.exists(self.model_path):
            print(f"Error: Model directory '{self.model_path}' not found.")
            return False

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            print(f"Model loaded successfully on {self.device}")
            return True
        except Exception as e:
            print(f"Failed to load model: {e}")
            return False

    def predict(self, text):
        if self.model is None or self.tokenizer is None:
            if not self.load_model():
                 return None

        # Check if text contains Arabic characters
        if not self.contain_arabic(text):
            return {
                "sentiment": "Unknown",
                "cleaned_text": text,
                "processed_text": text,
                "confidence": 0.0,
                "has_negation": False
            }

        cleaned_text = clean_text(text)
        text_with_negation = add_negation_feature(cleaned_text)

        # Use max_length=128 to match training configuration
        inputs = self.tokenizer(text_with_negation, return_tensors="pt", padding=True, truncation=True, max_length=128)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=-1).item()

        # Get confidence scores
        probabilities = torch.softmax(logits, dim=-1)[0]
        confidence = probabilities[predicted_class_id].item()

        # Label map from model.py: {'positive': 1, 'negative': 0}
        # So 0 is Negative, 1 is Positive
        sentiment = "Positive" if predicted_class_id == 1 else "Negative"
        has_neg = has_negation(cleaned_text)

        return {
            "sentiment": sentiment,
            "cleaned_text": cleaned_text,
            "processed_text": text_with_negation,
            "confidence": confidence,
            "has_negation": has_neg
        }

    @staticmethod
    def contain_arabic(text):
        """
        Check if the text contains Arabic characters.
        """
        if not text:
            return False
        for char in text:
            if '\u0600' <= char <= '\u06FF':
                return True
        return False
