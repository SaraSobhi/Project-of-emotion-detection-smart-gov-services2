# ML Service - Custom Model Integration Guide

This ML service provides a flexible structure for integrating your own machine learning models. The model-specific code has been removed, leaving you with a clean template to customize.

## Quick Start

### 1. Customize Preprocessing (`utils.py`)

Edit the three main functions in `utils.py`:

- **`clean_text(text)`**: Implement your text preprocessing logic
  - Remove special characters
  - Normalize text (lowercase, accents, etc.)
  - Language-specific cleaning
  
- **`has_negation(text)`**: Detect negation in your language (optional)
  - Add negation keywords for your language
  - Use regex patterns or NLP libraries
  
- **`add_negation_feature(text)`**: Add special features to text (optional)
  - Prepend/append special tokens
  - Modify text based on linguistic features

### 2. Customize Model Loading (`predict.py`)

Update the `ModelWrapper` class:

- **`__init__()`**: Set your model path
  - Default: `"my_model"` - change this to your model directory
  
- **`load_model()`**: Load your model
  - Current implementation uses HuggingFace transformers
  - Replace with your framework (PyTorch, TensorFlow, scikit-learn, etc.)
  
- **`predict(text)`**: Customize prediction logic
  - Adjust preprocessing steps
  - Update tokenization parameters
  - Modify label mapping for your classes
  - Customize return format

### 3. Update API Response Format

The current prediction returns:
```python
{
    "prediction": <class_id>,
    "cleaned_text": <preprocessed_text>,
    "processed_text": <text_with_features>,
    "confidence": <confidence_score>,
    "has_negation": <boolean>
}
```

Modify this in `predict.py` to match your needs (e.g., change `"prediction"` to `"sentiment"`, `"label"`, etc.).

### 4. Train Your Model

Update `train.py` to match your training pipeline, or remove it if you're using a pre-trained model.

## File Structure

```
ml_service/
├── app.py              # Flask API endpoints (minimal changes needed)
├── predict.py          # Model wrapper (CUSTOMIZE THIS)
├── utils.py            # Preprocessing utilities (CUSTOMIZE THIS)
├── train.py            # Training script (optional, customize or remove)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
└── README.md           # This file
```

## API Endpoints

- **POST `/predict`**: Make predictions
  ```json
  {
    "text": "your input text"
  }
  ```

- **POST `/train`**: Trigger model training (optional)
  ```json
  {
    "dataset_path": "path/to/dataset.csv"
  }
  ```

- **GET `/health`**: Check service health

## Example Customization

### For English Sentiment Analysis

**utils.py:**
```python
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Keep only letters
    return text.strip()

def has_negation(text):
    negation_words = ['not', 'no', 'never', 'neither', 'nobody', 'nothing']
    return any(word in text.lower().split() for word in negation_words)
```

**predict.py:**
```python
# In predict() method, update label mapping:
label_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
prediction = label_map[predicted_class_id]

return {
    "sentiment": prediction,
    "confidence": confidence,
    # ... other fields
}
```

## Running the Service

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Or use Docker
docker build -t ml-service .
docker run -p 5001:5001 ml-service
```

## Notes

- The `__pycache__` directory has been removed and will be regenerated when you run the service
- Make sure your model directory exists before starting the service
- Update `requirements.txt` if you need additional dependencies for your model
