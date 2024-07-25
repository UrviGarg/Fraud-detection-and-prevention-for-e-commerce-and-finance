import pandas as pd
from sklearn.preprocessing import LabelE/ncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
import matplotlib.pyplot as plt

# Load the data
mouse_df = pd.read_csv('mouse_data.csv')
keyboard_df = pd.read_csv('keyboard_data.csv')

# Add labels (0 for non-fraud, 1 for fraud) - ensure you have appropriate labeling in your real dataset
mouse_df['label'] = 0  # Adjust as necessary
keyboard_df['label'] = 0  # Adjust as necessary

# Encode categorical features
label_encoder = LabelEncoder()

for col in ['button']:  # Replace with the actual column names
    if col in mouse_df.columns:
        mouse_df[col] = label_encoder.fit_transform(mouse_df[col].astype(str))

for col in ['key']:  # Replace with the actual column names
    if col in keyboard_df.columns:
        keyboard_df[col] = label_encoder.fit_transform(keyboard_df[col].astype(str))

# Combine both dataframes
combined_df = pd.concat([mouse_df, keyboard_df], ignore_index=True)

# Fill NaN values if any
combined_df.fillna(0, inplace=True)

# Check for any non-numeric columns
non_numeric_cols = combined_df.select_dtypes(include=['object']).columns
print("Non-numeric columns:", non_numeric_cols)

# Features and labels
X = combined_df.drop('label', axis=1)
y = combined_df['label']

# Convert all features to numeric
X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# ROC AUC
y_prob = clf.predict_proba(X_test)
if y_prob.shape[1] > 1:
    roc_auc = roc_auc_score(y_test, y_prob[:, 1])
    fpr, tpr, thresholds = roc_curve(y_test, y_prob[:, 1])

    # Plot ROC curve
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()
else:
    print("ROC AUC score cannot be calculated because there is only one class present in the test set.")
