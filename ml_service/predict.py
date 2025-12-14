import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
from .utils import clean_text, has_negation, add_negation_feature

class ModelWrapper:
    def __init__(self, model_path="my_model"):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        """Load model and tokenizer. Customize for your model type."""
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
        """Make prediction. Customize preprocessing, inference, and output format."""
        if self.model is None or self.tokenizer is None:
            if not self.load_model():
                 return None

        # Preprocessing
        cleaned_text = clean_text(text)
        text_with_negation = add_negation_feature(cleaned_text)

        # Tokenization - adjust max_length for your model
        inputs = self.tokenizer(
            text_with_negation, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=128
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Inference
        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=-1).item()
        probabilities = torch.softmax(logits, dim=-1)[0]
        confidence = probabilities[predicted_class_id].item()

        # Customize label mapping for your classes
        prediction = predicted_class_id
        has_neg = has_negation(cleaned_text)

        # Customize return format for your API
        return {
            "prediction": prediction,
            "cleaned_text": cleaned_text,
            "processed_text": text_with_negation,
            "confidence": confidence,
            "has_negation": has_neg
        }

