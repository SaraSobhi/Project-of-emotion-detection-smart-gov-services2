import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import sys


def has_negation(text):
    """
    Word-based negation detection using token matching.
    """
    tokens = text.split()
    neg_set = set(ARABIC_NEGATIVE_KEYWORDS)

    return any(token in neg_set for token in tokens)

def add_negation_feature(text):
    """
    Appends a special token if negation is detected to help the model context.
    """
    if has_negation(text):
        return  "سئ " + text
    return text
# %% Cell
ARABIC_NEGATIVE_KEYWORDS = [
    # Basic negation particles
    'لا', 'لن', 'لم', 'ليس', 'ليست', 'ليسوا', 'لست', 'لسنا', 'لسن',
    'ما', 'غير', 'بدون', 'دون', 'بلا',

    # Colloquial/Egyptian negation (IMPORTANT for sarcasm)
    'محدش', 'مفيش', 'مافيش', 'ولا', 'مش', 'مو', 'موش',
    'ماحدش', 'محد', 'ماحد', 'مالوش', 'ملوش', 'مليش', 'ماليش',

    # Negative verbs and expressions
    'لا يوجد', 'لا توجد', 'لا اعتقد', 'لا افكر', 'لا اظن',
    'لا احب', 'لا اريد', 'لا استطيع', 'لا اقدر',
    'ما ينفعش', 'مينفعش', 'ما يصحش', 'مايصحش',

    # Negative adjectives and words
    'سيء', 'سيئ', 'سيئه', 'سيئين', 'فاشل', 'فشل', 'رديء', 'ردئ',
    'مقرف', 'قبيح', 'كريه', 'مزعج', 'محبط', 'مخيب',
    'ضعيف', 'سخيف', 'تافه', 'حقير', 'وحش', 'فظيع',
    'مرعب', 'مخيف', 'مؤلم', 'حزين', 'كئيب', 'محزن',
    'غاضب', 'زعلان', 'منزعج', 'مستاء', 'ساخط',
    'زباله', 'قمامه', 'خرا', 'تعبان', 'وسخ',

    # Negative phrases and warnings
    'لا يعجبني', 'لا يعجب', 'لا افضل', 'لا انصح', 'ما انصحش',
    'غير جيد', 'غير مقبول', 'غير صحيح', 'غير مناسب',
    'بدون فائده', 'بلا فائده', 'بلا معني', 'بدون معني',
    'ما تجربوش', 'ماتجربوش', 'ما تشتروش', 'ماتشتروش',
    'ما تنزلوش', 'ماتنزلوش', 'ينزله', 'تنزله', 'يشتريه', 'تشتريه',

    # Common negative expressions
    'للاسف', 'مع الاسف', 'يا للاسف', 'واحسرتاه',
    'مشكله', 'مشاكل', 'عيب', 'عيوب', 'خطا', 'اخطاء',
    'فاشل', 'خساره', 'خسران', 'ضرر', 'اضرار',
    'كارثه', 'كوارث', 'مصيبه', 'مصائب', 'ازمه', 'ازمات'
]



def predict_sentiment(text, model, tokenizer):
    cleaned_text = clean_text(text)
    text_with_negation = add_negation_feature(cleaned_text)

    # Use max_length=128 to match training configuration
    inputs = tokenizer(text_with_negation, return_tensors="pt", padding=True, truncation=True, max_length=128)

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_class_id = torch.argmax(logits, dim=-1).item()

    # Get confidence scores
    probabilities = torch.softmax(logits, dim=-1)[0]
    confidence = probabilities[predicted_class_id].item()

    # Label map from model.py: {'positive': 1, 'negative': 0}
    # So 0 is Negative, 1 is Positive
    sentiment = "Positive" if predicted_class_id == 1 else "Negative"
    has_neg = has_negation(cleaned_text)

    return sentiment, cleaned_text, text_with_negation, confidence, has_neg


def main():
    model_path = "my_gov_model"

    if not os.path.exists(model_path):
        print(f"Error: Model directory '{model_path}' not found.")
        print("Please run 'python model.py' first to train and save the model.")
        return

    print(f"Loading model from {model_path}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    print("Model loaded successfully!")
    print("Enter a sentence to predict its sentiment (or 'quit' to exit):")

    while True:
        user_input = input("\nInput: ")
        if user_input.lower() in ['quit', 'exit']:
            break

        if not user_input.strip():
            continue

        sentiment, cleaned, text_with_neg, confidence, has_neg = predict_sentiment(user_input, model, tokenizer)
        print(f"Cleaned Text: {cleaned}")
        print(f"Processed Text: {text_with_neg}")
        print(f"Contains Negation: {'Yes' if has_neg else 'No'}")
        print(f"Prediction: {sentiment} (Confidence: {confidence*100:.2f}%)")

if __name__ == "__main__":
    main()


