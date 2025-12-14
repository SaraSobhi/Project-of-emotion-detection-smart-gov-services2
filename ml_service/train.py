import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, EarlyStoppingCallback
from datasets import Dataset
import torch
from sklearn.metrics import accuracy_score, f1_score
from .utils import clean_text
import os

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    acc = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average='weighted')
    return {"accuracy": acc, "f1": f1}

def tokenize_function(examples, tokenizer):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=64)

def train_model(dataset_path, output_dir="my_model"):
    print(f"Loading dataset from {dataset_path}...")
    try:
        df = pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return False, str(e)

    # Basic preprocessing
    if 'clean_text' not in df.columns:
         df['clean_text'] = df['text'].apply(clean_text) if 'text' in df.columns else df.iloc[:, 0].apply(clean_text)

    # Assume binary classification if labeling not present or customize mapping
    # Users should customize this part
    if 'label' in df.columns and df['label'].dtype == 'object':
        unique_labels = df['label'].unique()
        label_map = {label: i for i, label in enumerate(unique_labels)}
        df['label_id'] = df['label'].map(label_map)
    elif 'label_id' not in df.columns:
         # Fallback or error
         pass

    df.dropna(inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(
        df['clean_text'], df['label_id'], test_size=0.2, random_state=42
    )

    train_dataset = Dataset.from_pandas(
        pd.DataFrame({
            "text": X_train,
            "labels": y_train.astype("int64")
        })
    )
    test_dataset = Dataset.from_pandas(
        pd.DataFrame({
            "text": X_test,
            "labels": y_test.astype("int64")
        })
    )

    # generic model
    model_name = "bert-base-uncased" 
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(df['label_id'].unique()))

    encoded_train = train_dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)
    encoded_test = test_dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)

    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        fp16=torch.cuda.is_available(),
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=encoded_train,
        eval_dataset=encoded_test,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    trainer.train()

    results = trainer.evaluate()
    print(f"Final Results: {results}")

    print(f"Saving model to {output_dir}...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    return True, results
