import torch
import torch.nn as nn
import torch.optim as optim
from model import NeuralNet
from utils import bag_of_words, tokenize, stem  # Ensure tokenize and other utils are imported
import json
import numpy as np

# Load intents file
with open('intents.json', 'r') as f:
    intents = json.load(f)

# Prepare the dataset
all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        words = tokenize(pattern)
        all_words.extend(words)
        xy.append((words, tag))

# Stem and remove duplicates
all_words = sorted(set([stem(w) for w in all_words if w not in ['?', '!', '.', ',']]))
tags = sorted(set(tags))

# Prepare training data
X_train = []
y_train = []

for (pattern_words, tag) in xy:
    bag = bag_of_words(pattern_words, all_words)
    X_train.append(bag)
    y_train.append(tags.index(tag))

X_train = np.array(X_train)
y_train = np.array(y_train)

# Convert to tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)

# Create the model
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)

model = NeuralNet(input_size, hidden_size, output_size)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training the model
epochs = 1000
for epoch in range(epochs):
    output = model(X_train)
    loss = criterion(output, y_train)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

# Save the trained model
torch.save(model.state_dict(), "model.pth")
print("Model training complete and saved.")

# Save all_words and tags (for use in app.py)
train_data = {"all_words": all_words, "tags": tags}
with open("train_data.json", "w") as f:
    json.dump(train_data, f)
print("All words and tags saved.")