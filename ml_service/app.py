from flask import Flask, request, jsonify
from predict import ModelWrapper
from train import train_model
import threading

app = Flask(__name__)

# Initialize model wrapper
# We won't load the model immediately if it doesn't exist yet (first run)
model_wrapper = ModelWrapper()
if model_wrapper.load_model():
    print("Model loaded at startup.")
else:
    print("Model not found at startup. Please train first.")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data['text']
    result = model_wrapper.predict(text)
    
    if result is None:
        return jsonify({"error": "Model not loaded. Please train the model first."}), 503

    return jsonify(result)

def run_training_background(dataset_path):
    # This logic assumes we want to train in background and then reload the model
    success, metrics = train_model(dataset_path)
    if success:
        print("Training completed successfully. Reloading model...")
        model_wrapper.load_model()
    else:
        print(f"Training failed: {metrics}")

@app.route('/train', methods=['POST'])
def train():
    data = request.get_json()
    dataset_path = data.get('dataset_path', 'dataset.csv')
    
    # Simple check if already training could be added here, but keeping it simple as requested
    
    # Run training in a separate thread to avoid blocking the response
    thread = threading.Thread(target=run_training_background, args=(dataset_path,))
    thread.start()
    
    return jsonify({"message": "Training started in background", "dataset": dataset_path})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "model_loaded": model_wrapper.model is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
