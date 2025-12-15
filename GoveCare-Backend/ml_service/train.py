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

def train_model(dataset_path, output_dir="my_gov_model"):
    print(f"Loading dataset from {dataset_path}...")
    try:
        df = pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return False, str(e)

    df['clean_text'] = df['text'].apply(clean_text)

    label_map = {'positive': 1, 'negative': 0}
    df['label_id'] = df['label'].map(label_map)

    df.dropna(subset=['clean_text', 'label_id'], inplace=True)
    df = df[df['clean_text'].str.len() > 2]

    X_train, X_test, y_train, y_test = train_test_split(
        df['clean_text'], df['label_id'], test_size=0.2, random_state=42, stratify=df['label_id']
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

    model_name = "aubmindlab/bert-base-arabertv02-twitter"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    model.config.problem_type = "single_label_classification"

    encoded_train = train_dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)
    encoded_test = test_dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)

    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=4,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        gradient_accumulation_steps=2,
        learning_rate=1.5e-5,
        warmup_ratio=0.1,
        weight_decay=0.01,
        lr_scheduler_type="linear",
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        fp16=torch.cuda.is_available(), 
        max_grad_norm=1.0,
        logging_strategy="steps",
        logging_steps=100,
        seed=42,
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

    results_bert = trainer.evaluate()
    acc_arabert = results_bert['eval_accuracy']
    f1_arabert = results_bert['eval_f1']

    print("\nAraBERT Final Results:")
    print(f"   - Accuracy: {acc_arabert*100:.2f}%")
    print(f"   - F1 Score: {f1_arabert*100:.2f}%")

    print(f"Saving model to {output_dir}...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    return True, {"accuracy": acc_arabert, "f1": f1_arabert}