#!/usr/bin/env python3
from src.initial_data_preparation import prepare_data
from src.optimize_features import optimize_features
from src.training_GBC_model import train_model


def main():
    """
    Main pipeline for data preparation, feature selection, and model training.

    Steps:
    1. Prepare raw data and add class labels.
    2. Perform feature selection using Recursive Feature Elimination.
        - Run RFE loop to find the optimal number of features.
        - Specify no. of features to be used for training.
    3. Train a Gradient Boosting Classifier (GBC) model.
    """
    
    print("\nStart data preparation...")
    prepare_data()
    
    print("\nSelecting features to be used for training...")
    optimize_features(run_RFE_loop=False, no_features=15)

    print("\nTraining the model...")
    train_model()
    
if __name__ == '__main__':
    main()