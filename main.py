#!/usr/bin/env python3
import argparse
import os
import shutil
import pandas as pd
import cv2
import joblib
from datetime import datetime

class FlowCamPaths:
    def __init__(self, raw_dir):
        self.raw_dir = os.path.abspath(raw_dir)
        self.sample_name = os.path.basename(self.raw_dir)
        self.output_dir = os.path.join(self.raw_dir, 'output')
        self.extract_dir = os.path.join(self.output_dir, 'Extracted_images')
        self.predicted_dir = os.path.join(self.output_dir, 'Predicted_images')
        self.predicted_junk_dir = os.path.join(self.predicted_dir, 'Junk')
        self.predicted_missed_dir = os.path.join(self.predicted_dir, 'Missed')
        self.predicted_protist_dir = os.path.join(self.predicted_dir, 'Protist')
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(self.script_path, 'trained_gbc_model.pkl')

    def prepare_output_dirs(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
            print("Previous output directory is replaced.")
        os.makedirs(self.extract_dir)
        os.makedirs(self.predicted_dir)
        os.makedirs(self.predicted_junk_dir)
        os.makedirs(self.predicted_missed_dir)
        os.makedirs(self.predicted_protist_dir)

class FlowCamReportGenerator:
    def __init__(self, raw_dir, output_dir, predicted_dirs):
        self.raw_dir = raw_dir
        self.output_dir = output_dir
        self.predicted_junk_dir = predicted_dirs["junk"]
        self.predicted_missed_dir = predicted_dirs["missed"]
        self.predicted_protist_dir = predicted_dirs["protist"]
        self.sample_name = os.path.basename(os.path.normpath(raw_dir))
        self.sample_volume = self._get_sample_volume()

    # '_' is used to indicate that this method is private
    def _get_sample_volume(self):
        # DEAL WITH ERRORS
        summary_files = [file for file in os.listdir(self.raw_dir) if file.endswith("_summary.csv")]
        for summary_file in summary_files:
            with open(os.path.join(self.raw_dir, summary_file), 'r') as file:
                for line in file:
                    if 'Sample Volume Imaged ml' in line:
                        return float(line.split(',')[1].strip())

    def generate_report(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        count_junk = len(os.listdir(self.predicted_junk_dir))
        count_missed = len(os.listdir(self.predicted_missed_dir))
        count_protist = len(os.listdir(self.predicted_protist_dir))

        report_content = [
            f" Report - {self.sample_name} \t ({current_time})",
            "=========================",
            f"Sample Volume Imaged (ml): {self.sample_volume}",
            "\nCategories",
            f"Junk: {count_junk}",
            f"Missed: {count_missed}",
            f"Protist: {count_protist}",
            f"\nEstimated conc. (protists/ml): {count_protist / self.sample_volume:.2f}",
            f"\n{self.sample_name}\t{self.sample_volume}\t{count_junk}\t{count_missed}\t{count_protist}\t{count_protist / self.sample_volume:.2f}"
        ]

        with open(os.path.join(self.output_dir, 'report.txt'), 'w') as report_file:
            for line in report_content:
                report_file.write(line + '\n')

        print(f"Report created for {self.sample_name} in 'Output' directory")

class FlowCamProcessor:
    def __init__(self, raw_dir):
        self.paths = FlowCamPaths(raw_dir)
        self.paths.prepare_output_dirs()

    def generate_report(self):
        predicted_dirs = {
            "junk": self.paths.predicted_junk_dir,
            "missed": self.paths.predicted_missed_dir,
            "protist": self.paths.predicted_protist_dir
        }

        report_generator = FlowCamReportGenerator(
            self.paths.raw_dir,
            self.paths.output_dir,
            predicted_dirs
        )
        report_generator.generate_report()

    def run(self):
        image_separator(self.paths.raw_dir, self.paths.extract_dir)
        run_classifier(
            self.paths.raw_dir, self.paths.model_path,
            self.paths.extract_dir, self.paths.predicted_junk_dir,
            self.paths.predicted_missed_dir, self.paths.predicted_protist_dir
        )

        self.generate_report()


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
        ID = file.split('_')[-1].split('.')[0]
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-raw_dir', '--raw_directory', type=str, required=True)
    args = parser.parse_args()

    processor = FlowCamProcessor(args.raw_directory)
    processor.run()



if __name__ == "__main__":
    main()
