#!/usr/bin/env python3

import argparse
import os
import shutil
import pandas as pd
import cv2
import joblib
from datetime import datetime

def dir_setup(raw_directory):
    raw_directory = os.path.normpath(raw_directory)
    sample_name = os.path.basename(raw_directory)
    output_dir_name = f'Output_{sample_name}'

    #path_current = os.getcwd()
    #path_raw = os.path.join(path_current, raw_directory)
    path_raw = os.path.abspath(raw_directory)
    #path_output = os.path.join(path_current, output_dir_name)
    path_output = os.path.join(os.path.dirname(path_raw), output_dir_name)
    path_extracted_imgs = os.path.join(path_output, 'Extracted_images')
    path_predicted_imgs = os.path.join(path_output, 'Predicted_images')
    path_predicted_junk = os.path.join(path_predicted_imgs, 'Junk')
    path_predicted_missed = os.path.join(path_predicted_imgs, 'Missed')
    path_predicted_protist = os.path.join(path_predicted_imgs, 'Protist')
    path_script = os.path.dirname(os.path.abspath(__file__))
    path_model = os.path.join(path_script, 'trained_gbc_model.pkl')

    if os.path.exists(path_output):
        shutil.rmtree(path_output)
        print("Previous output directory is replaced.")

    os.makedirs(path_output)
    os.makedirs(path_extracted_imgs)
    os.makedirs(path_predicted_imgs)
    os.makedirs(path_predicted_junk)
    os.makedirs(path_predicted_missed)
    os.makedirs(path_predicted_protist)

    return {
        'path_raw': path_raw,
        'path_output': path_output,
        'path_extracted_imgs': path_extracted_imgs,
        'path_predicted_junk': path_predicted_junk,
        'path_predicted_missed': path_predicted_missed,
        'path_predicted_protist': path_predicted_protist,
        'path_model': path_model
    }

def image_separator(path_raw, path_extracted_imgs):
    try:
        os.chdir(path_raw)
    except FileNotFoundError:
        print(f'Error: {path_raw} not found')
        return

    for filename in [f for f in os.listdir(path_raw) if f.endswith(".lst")]:
        sample_name = os.path.splitext(filename)[0]
        sample_outpath = path_extracted_imgs
        fp = os.path.join(path_raw, filename)
        header = pd.read_csv(fp, sep='|', skiprows=1, nrows=65)
        hd = list(header["num-fields"])
        meta = pd.read_csv(fp, sep='|', skiprows=67, header=None)
        meta.columns = hd
        loaded_cp = "not_loaded"
        for id in meta["id"]:
            i = id - 1
            collage_filename = meta["collage_file"][i]
            cp = os.path.join(path_raw, collage_filename)

            if cp != loaded_cp:
                collage = cv2.imread(cp)
                loaded_cp = cp
            img_sub = collage[meta["image_y"][i]:(meta["image_y"][i] + meta["image_h"][i]),
                              meta["image_x"][i]:(meta["image_x"][i] + meta["image_w"][i])]

            vp = os.path.join(sample_outpath, f"{sample_name}_{meta['image_id'][i]}.png")
            cv2.imwrite(vp, img_sub)
    print("Images extracted from collage files")

def run_classifier(path_raw, path_model, path_extracted_imgs, path_pred_junk, path_pred_missed, path_pred_protist):
    csv_file = os.path.join(path_raw, f"{os.path.basename(path_raw)}.csv")
    df = pd.read_csv(csv_file)
    model = joblib.load(path_model)

    features = ['Area (Filled)', 'Aspect Ratio', 'Circle Fit', 'Circularity', 'Circularity (Hu)', 'Compactness', 'Diameter (FD)', 
                'Edge Gradient', 'Elongation', 'Geodesic Aspect Ratio', 'Geodesic Thickness', 'Intensity', 'Ratio Red/Blue', 
                'Roughness', 'Transparency']

    predictions = model.predict(df[features])
    df['Predictions'] = predictions
    mapping = {0: 'Junk', 1: 'Missed', 2: 'Protist'}
    df['Predictions'] = df['Predictions'].map(mapping)

    for file in os.listdir(path_extracted_imgs):
        path_file = os.path.join(path_extracted_imgs, file)
        ID = file.split('_')[1].split('.')[0]
        prediction_series = df.loc[df['Original Reference ID'] == ID, "Predictions"]

        if not prediction_series.empty:
            prediction = prediction_series.iloc[0]
            if prediction == 'Protist':
                dest_path = os.path.join(path_pred_protist, file)
            elif prediction == 'Junk':
                dest_path = os.path.join(path_pred_junk, file)
            elif prediction == 'Missed':
                dest_path = os.path.join(path_pred_missed, file)
            else:
                continue

            shutil.move(path_file, dest_path)

    os.rmdir(path_extracted_imgs)
    print("Images predicted and sorted in 'Prediction' directory.\n")

def report_file(path_raw, path_output, path_pred_junk, path_pred_missed, path_pred_protist):
    summary_files = [file for file in os.listdir(path_raw) if file.endswith("_summary.csv")]

    for summary_file in summary_files:
        with open(os.path.join(path_raw, summary_file), 'r') as file:
            for line in file:
                if 'Sample Volume Imaged ml' in line:
                    volume_imaged = float(line.split(',')[1].strip())

    sample = os.path.basename(os.path.normpath(path_raw))
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    count_junk = len(os.listdir(path_pred_junk))
    count_missed = len(os.listdir(path_pred_missed))
    count_protist = len(os.listdir(path_pred_protist))

    report_content = [
        f" Report - {sample} \t ({current_time})",
        "=========================",
        f"Sample Volume Imaged (ml): {volume_imaged}",
        "\nCategories",
        f"Junk: {count_junk}",
        f"Missed: {count_missed}",
        f"Protist: {count_protist}",
        f"\nEstimated conc. (protists/ml): {count_protist / volume_imaged:.2f}",
        f"\n{sample}\t{volume_imaged}\t{count_junk}\t{count_missed}\t{count_protist}\t{count_protist / volume_imaged:.2f}"
    ]

    with open(os.path.join(path_output, 'report.txt'), 'w') as report_file:
        for line in report_content:
            report_file.write(line + '\n')

    print(f'Sample: {sample}')
    print(f'Sample Volume Imaged (ml): {volume_imaged}')
    print(f'Estimated conc. (protists/ml): {count_protist / volume_imaged:.2f}')
    print("Report created in 'Output' directory")

def main():
    parser = argparse.ArgumentParser(description="Separate images based on directory path.")
    parser.add_argument('-raw_dir', '--raw_directory', type=str, required=True,
                        help='The path to the directory containing the raw data files (csv, tif)')
    args = parser.parse_args()
    raw_directory = args.raw_directory

    paths = dir_setup(raw_directory)
    image_separator(paths['path_raw'], paths['path_extracted_imgs'])
    run_classifier(paths['path_raw'], paths['path_model'], paths['path_extracted_imgs'], 
                   paths['path_predicted_junk'], paths['path_predicted_missed'], paths['path_predicted_protist'])
    report_file(paths['path_raw'], paths['path_output'], paths['path_predicted_junk'], 
                paths['path_predicted_missed'], paths['path_predicted_protist'])

if __name__ == "__main__":
    main()
