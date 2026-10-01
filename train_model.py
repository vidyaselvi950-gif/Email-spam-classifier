import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix
import joblib
import os
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv(
    "data/SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"]
)

# Convert labels
data["label"] = data["label"].map({"ham": 0, "spam": 1})

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    data["message"],
    data["label"],
    test_size=0.2,
    random_state=42,
    stratify=data["label"]
)

# Create ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english")),
    ("classifier", MultinomialNB())
])
logistic_model = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english")),
    ("classifier", LogisticRegression(max_iter=1000))
])
logistic_model = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english")),
    ("classifier", LogisticRegression(max_iter=1000))
])

svm_model = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english")),
    ("classifier", SVC())
])

# Train model
model.fit(X_train, y_train)
logistic_model.fit(X_train, y_train)
svm_model.fit(X_train, y_train)
# Test model
predictions = model.predict(X_test)
logistic_predictions = logistic_model.predict(X_test)
svm_predictions = svm_model.predict(X_test)

# Display results
accuracy = accuracy_score(y_test, predictions)
cm = confusion_matrix(y_test, predictions)

false_positives = cm[0][1]
true_negatives = cm[0][0]

false_positive_rate = false_positives / (false_positives + true_negatives)

print(f"False Positive Rate: {false_positive_rate * 100:.2f}%")
logistic_accuracy = accuracy_score(y_test, logistic_predictions)
svm_accuracy = accuracy_score(y_test, svm_predictions)

print(f"SVM Accuracy: {svm_accuracy * 100:.2f}%")
print(f"Logistic Regression Accuracy: {logistic_accuracy * 100:.2f}%")
print("Email Spam Classifier")
print("---------------------")
print(f"Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Create model folder
os.makedirs("model", exist_ok=True)

# Save trained model
joblib.dump(model, "model/spam_classifier.pkl")

print("\nModel saved successfully!")
print("Location: model/spam_classifier.pkl")

# Spam keyword visualization
spam_messages = data[data["label"] == 1]["message"]

all_spam_text = " ".join(spam_messages)

words = all_spam_text.lower().split()

word_counts = pd.Series(words).value_counts().head(15)
plt.figure(figsize=(10, 6))
word_counts.plot(kind="bar")

plt.title("Top 15 Spam-Indicating Keywords")
plt.xlabel("Keywords")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
plt.figure(figsize=(10, 6))
word_counts.plot(kind="bar")

plt.title("Top 15 Spam-Indicating Keywords")
plt.xlabel("Keywords")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()