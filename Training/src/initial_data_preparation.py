#!/usr/bin/env python3

import os
import pandas as pd

def prepare_data():
    '''
    This function prepares the data for the project by loading the training datasets and the manually classified images.
    '''
    
    
    # Load the training datasets
    dataset_1 = pd.read_csv('data/raw/7-Pygsuia-SF-SW-NITRATE-day5-sample3-replicate3-08April2024/7-Pygsuia-SF-SW-NITRATE-day5-sample3-replicate3-08April2024.csv')
    dataset_2 = pd.read_csv('data/raw/7-Pygsuia-SF-SW-sulfate-day5-sample2-replicate3-08April2024/7-Pygsuia-SF-SW-sulfate-day5-sample2-replicate3-08April2024.csv')
    dataset_3 = pd.read_csv('data/raw/7-Pygsuia-SF-SW-sulfate-day5-sample3-replicate3A-08April2024/7-Pygsuia-SF-SW-sulfate-day5-sample3-replicate3A-08April2024.csv')

    # Add a column to identify the dataset
    dataset_1['Dataset'] = 'dataset_1'
    dataset_2['Dataset'] = 'dataset_2'
    dataset_3['Dataset'] = 'dataset_3'

    df = pd.concat([dataset_1, dataset_2, dataset_3], ignore_index=True)

    # Images from the three datasets are manually classified into the following classes
    junk_df = pd.DataFrame({'Class' : 'Junk',
                'File_name' : os.listdir('data/classes/Junk/'),
                'Original Reference ID' : [f.split('_')[-1].split('.')[0] for f in os.listdir('data/classes/Junk/')]})

    missed_df = pd.DataFrame({'Class' : 'Missed',
                'File_name' : os.listdir('data/classes/Missed/'),
                'Original Reference ID' : [f.split('_')[-1].split('.')[0] for f in os.listdir('data/classes/Missed/')]})

    protist_df = pd.DataFrame({'Class' : 'Protist',
                'File_name' : os.listdir('data/classes/Protist/'),
                'Original Reference ID' : [f.split('_')[-1].split('.')[0] for f in os.listdir('data/classes/Protist/')]})

                            
    # Concatenate the three Class dataframes
    df_classes = pd.concat([junk_df, missed_df, protist_df], ignore_index=True)

    # Merge the columns containing the classes with the main dataframe
    df = pd.merge(df, df_classes, on='Original Reference ID', how='left')

    # Save the prepared data
    df.to_csv('data/initial_data_preparation.csv', index=False)
    print('Data preparation completed, saved as initial_data_preparation.csv')
    
if __name__ == '__main__':
    prepare_data()