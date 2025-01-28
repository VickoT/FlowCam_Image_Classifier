import pandas as pd
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
from sklearn.metrics import accuracy_score

def optimize_features(run_RFE_loop=False, no_features=15):

    df_featureSel = pd.read_csv('data/initial_data_preparation.csv')
    
    X = df_featureSel.select_dtypes(include=['number'])
    y = df_featureSel['Class']
    
    # Encode string labels to integers (0, 1, 2)
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, stratify=y, random_state=42)
    
    # Define the RFE estimator
    estimator = RandomForestClassifier(n_jobs=-1)
    
    if run_RFE_loop:
        start_time = time.time()
        for k in range(20,2,-1):
            rfe = RFE(estimator=estimator, n_features_to_select=k, step=1)
            rfe.fit(X_train,y_train)
        
            X_train_rfe = rfe.transform(X_train)
            X_test_rfe = rfe.transform(X_test)
        
            # Fit the model on the reduced set of features
            estimator.fit(X_train_rfe, y_train)
            y_pred = estimator.predict(X_test_rfe)
            accuracy = accuracy_score(y_test, y_pred)
            print(f'Selected features: {k}, accuracy: {accuracy:.2f} Elapsed time: {time.time() - start_time:.2f}')
        print(f'Total elapsed time: {time.time() - start_time:.2f}')
    
    # Define the optimal number of features based on the above analysis
    selected_num_features = no_features
    
    # Fit RFE with the optimal number of features
    rfe = RFE(estimator=estimator, n_features_to_select=selected_num_features, step=1)
    rfe.fit(X_train, y_train)
    
    # Get the selected features
    selected_features = X.columns[rfe.support_]
    print(f"Selected features (tot. {selected_num_features}):")
    for i in selected_features.tolist(): print('\t' + i)
        
    # Save the selected features to a CSV file
    selected_features.to_series().to_csv('data/selected_features.csv', index=False, header=False)

  
if __name__ == '__main__':
    optimize_features(no_features=2)  