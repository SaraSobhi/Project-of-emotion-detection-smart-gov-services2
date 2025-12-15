import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from transformers import EarlyStoppingCallback
from datasets import Dataset
import torch
from sklearn.metrics import accuracy_score, f1_score

df = pd.read_csv('arabic_twitter_dataset.csv')

def clean_text(text):
    text = str(text)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("g", "q", text)
    text = re.sub(r'[^\u0600-\u06ff\u0750-\u077f\ufb50-\ufdff\ufe70-\ufeff\s]', '', text)
    return text.strip()

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

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=64)

encoded_train = train_dataset.map(tokenize_function, batched=True)
encoded_test = test_dataset.map(tokenize_function, batched=True)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    acc = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average='weighted')
    return {"accuracy": acc, "f1": f1}

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

    fp16=True,
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

output_dir = "my_gov_model"
print(f"Saving model to {output_dir}...")
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

