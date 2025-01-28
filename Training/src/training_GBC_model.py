import pandas as pd
import joblib 
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay

# Import the data
def train_model():
    df = pd.read_csv("data/initial_data_preparation.csv")
    selected_features = pd.read_csv("data/selected_features.csv", header=None)[0].tolist()

    # Select the features and the target
    X = df[selected_features]
    y = df['Class']

    # Encode string labels to integers
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, stratify=y, random_state=42)

    # Assign the data to new variables reserved for the Gradient Booster Classifier
    X_train_GBC, X_test_GBC, y_train_GBC, y_test_GBC = X_train.copy(), X_test.copy(), y_train.copy(), y_test.copy()

    # Train and fit the model
    gbc = GradientBoostingClassifier(n_estimators=500, max_depth=5, random_state=42)
    gbc.fit(X_train_GBC, y_train_GBC)
    # Save the model as a pickle file
    joblib.dump(gbc, 'trained_gbc_model.pkl')

    # Predict the test data for evaluation
    gbc_preds = gbc.predict(X_test_GBC)
    gbc_f1_score_all = round(f1_score(y_test_GBC, gbc_preds, average='weighted'), 3)
    print(f'GBC weighted F1-score: {gbc_f1_score_all}')

    # Generate the confusion matrix
    conf_matrix_gbc = confusion_matrix(y_test_GBC, gbc_preds)
    disp_gbc = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_gbc, display_labels=label_encoder.classes_)
    disp_gbc.plot()
    plt.title('Confusion Matrix - Gradient Booster Classifier')
    plt.show()
    
if __name__ == '__main__':
    train_model()