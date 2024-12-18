#install and import lib
!pip install transformers
!pip install torch
!pip install datasets

import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from transformers import DataCollatorWithPadding
from datasets import Dataset

# Add category, training dataset and test terms
categories = [
    "Operating Systems", "Networks", "Databases", "Data Structures",
    "Algorithms", "Software Engineering", "Programming Languages", "AI/ML"
]

data = {
    "term": [
        "HTTP", "TCP/IP", "MySQL", "Binary Search", "QuickSort", "Agile Methodology", "Python", "Linked List",
        "REST API", "NoSQL", "Linux", "Dynamic Programming", "PostgreSQL", "DNS", "Merge Sort", "Scrum", "JavaScript",
        "Trie", "HTTPS", "Docker"
    ],
    "category": [
        "Networks", "Networks", "Databases", "Algorithms", "Algorithms",
        "Software Engineering", "Programming Languages", "Data Structures", "Networks",
        "Databases", "Operating Systems", "Algorithms", "Databases", "Networks",
        "Algorithms", "Software Engineering", "Programming Languages", "Data Structures",
        "Networks", "Software Engineering"
    ]
}

test_terms = [
    "HTTP", "Kubernetes", "TensorFlow", "React", "Blockchain",
    "5G Networks", "Docker", "Encryption", "C#", "Sorting Algorithms",
    "GitHub", "Lambda Function", "SQL", "Machine Learning",
    "Microservices", "RSA Algorithm", "Big Data", "Neural Networks",
    "Assembly Language", "IPv6"
]

#pd화
df = pd.DataFrame(data)
df['category'] = pd.Categorical(df['category'], categories=categories, ordered=True)

# Encode category, Map with Label
df['label'] = df['category'].cat.codes

# Map label-category
label2id = {label: idx for idx, label in enumerate(categories)}
id2label = {idx: label for label, idx in label2id.items()}

# Split dataset
train_df, eval_df = train_test_split(df, test_size=0.2, random_state=42)

train_dataset = Dataset.from_pandas(train_df)
eval_dataset = Dataset.from_pandas(eval_df)

#Tokenize the dataset
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def tokenize_function(examples):
    return tokenizer(examples['term'], padding='max_length', truncation=True)

train_dataset = train_dataset.map(tokenize_function, batched=True)
eval_dataset = eval_dataset.map(tokenize_function, batched=True)

# Load Model
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(categories))

# Data Collator
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Create Train
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_strategy="no",
    report_to=[]
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Train
trainer.train()


# Predict test terms, Print
test_df = pd.DataFrame(test_terms, columns=['term'])
test_dataset = Dataset.from_pandas(test_df)
test_dataset = test_dataset.map(tokenize_function, batched=True)

predictions = trainer.predict(test_dataset)
pred_labels = torch.argmax(torch.tensor(predictions.predictions), axis=1)

test_df['Predicted Category'] = [id2label[label.item()] for label in pred_labels]
print(test_df)
