import csv
import math

def entropy(data):
    labels = [row[-1] for row in data]
    unique_labels = set(labels)
    ent = 0
    for label in unique_labels:
        p = labels.count(label) / len(labels)
        ent -= p * math.log2(p)
    return ent

def info_gain(data, attribute_index):
    total_entropy = entropy(data)
    values = set(row[attribute_index] for row in data)
    weighted_entropy = 0
    for value in values:
        subset = [row for row in data if row[attribute_index] == value]
        weighted_entropy += (len(subset) / len(data)) * entropy(subset)
    return total_entropy - weighted_entropy

def id3(data, attributes, headers):
    labels = [row[-1] for row in data]
    if len(set(labels)) == 1:
        return labels[0]
    if not attributes:
        return max(set(labels), key=labels.count)
    gains = [info_gain(data, i) for i in attributes]
    best_attr_index = attributes[gains.index(max(gains))]
    best_attr = headers[best_attr_index]
    tree = {best_attr: {}}
    remaining_attrs = [a for a in attributes if a != best_attr_index]
    values = set(row[best_attr_index] for row in data)
    for value in values:
        subset = [row for row in data if row[best_attr_index] == value]
        tree[best_attr][value] = id3(subset, remaining_attrs, headers)
    return tree

def print_tree(tree, indent=0):
    for key, value in tree.items():
        print('  ' * indent + str(key))
        if isinstance(value, dict):
            print_tree(value, indent + 1)
        else:
            print('  ' * (indent + 1) + str(value))

def predict(tree, instance, headers):
    if not isinstance(tree, dict):
        return tree
    attr = list(tree.keys())[0]
    attr_index = headers.index(attr)
    value = instance[attr_index]
    if value in tree[attr]:
        return predict(tree[attr][value], instance, headers)
    else:
        return "unknown"

# Load data
data = []
with open('tenis.csv', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        data.append(row)

attributes = list(range(len(headers)-1))
tree = id3(data, attributes, headers)
print("Decision Tree:")
print_tree(tree)

print("\nPredictions for some data:")
# Example 1: sunny,hot,high,FALSE -> no
instance1 = ['sunny', 'hot', 'high', 'FALSE']
pred1 = predict(tree, instance1, headers)
print(f"sunny, hot, high, FALSE -> {pred1}")

# Example 2: overcast, cool, normal, TRUE -> yes
instance2 = ['overcast', 'cool', 'normal', 'TRUE']
pred2 = predict(tree, instance2, headers)
print(f"overcast, cool, normal, TRUE -> {pred2}")

# Example 3: rainy, mild, high, FALSE -> yes
instance3 = ['rainy', 'mild', 'high', 'FALSE']
pred3 = predict(tree, instance3, headers)
print(f"rainy, mild, high, FALSE -> {pred3}")