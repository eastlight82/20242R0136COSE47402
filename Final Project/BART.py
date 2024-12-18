#Install, Import lib
!pip install transformers
!pip install torch
!pip install transformers pandas
from transformers import pipeline
import pandas as pd

# Zero-Shot Classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Add category
categories = [
    "Operating Systems",
    "Networks",
    "Databases",
    "Data Structures",
    "Algorithms",
    "Software Engineering",
    "Language",
    "AI/ML"
]

# Add term
terms = [
    "HTTP", "Kubernetes", "TensorFlow", "React", "Blockchain",
    "5G Networks", "Docker", "Encryption", "C#", "Sorting Algorithms",
    "GitHub", "Lambda Function", "SQL", "Machine Learning",
    "Microservices", "RSA Algorithm", "Big Data", "Neural Networks",
    "Assembly Language", "IPv6"
]

# Classify Term
for term in terms:
    result = classifier(term, categories)
    predicted_category = result['labels'][0]
    print(f"{term}: {predicted_category}")
