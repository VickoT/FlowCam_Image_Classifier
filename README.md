# ImageClassifier
**Author:** Viktor Törnblom

## Introduction
ImageClassifier is a Python-based application designed for classifying images
using a pre-trained machine learning algorithm. It is specifically tailored for processing
FlowCam output and categorizing images of particles into one of the following
three classes:

* Junk: Particles clearly defined as not being cells.
* Missed: Particles that are difficult to categorize (these are considered “Junk” when estimating the concentration).
* Protists: Images of particles resembling protist cells.

### About the classifier



## Prerequisites
- Anaconda or Miniconda

## Installation

*  Create and activate the conda environment:

```
conda create -n image_classifier python=3.12
conda activate image_classifier
```
 * Install required modules:

```
conda install pandas scikit-learn
pip install opencv-python
```

## Run ImageClassifier

```
conda activate image_classifier
\path\to\script\.ImageClassifier.py -raw_dir FlowCam_raw_dir
```

'FlowCam_raw_dir' should contain the raw FlowCam output data (the script uses the tif files and the metadata CSV file).

The following directory will be generated after running the script, where the
subdirectories 'Junk', 'Missed' and 'Protist' contain the images sorted into
their corresponding class. 

```
└── Output_example_dir
    ├── report.txt
    └── Predicted_images
        ├── Junk
        ├── Missed
        └── Protist
```

#### Manual reclassification

In case you are unsatisfied with the classification made by the classifier, you
may reclassify the images manually. This is done by moving the images in the
'Predicted_images' directory into the folder you find suitable. Then run the
script `re_eval.py` inside the **Output_example_dir**. The new stats will be
appended to the report file:

```
 Report - 4-LRM1b-day0-2         (2024-06-26 10:52)
=========================
Sample Volume Imaged (ml): 0.01773

Categories
Junk: 420
Missed: 21
Protist: 559

Estimated conc. (protists/ml): 31528.48

---------------------------------------------------------------
Manual reclassification          (2024-06-26 10:56)

Categories
Junk: 416
Missed: 21
Protist: 565

Estimated conc. (protists/ml): 31866.89
```

#### Help scripts

The `ImageClassifier.py` and `re_eval.py` scripts are designed to take a single
directory as input; however, there are often cases where you need to classify
multiple datasets. Therefore, bash scripts were created to loop over datasets in
a directory:

*  **loop_script.sh** - running `ImageClassifier.py` on all subdirectories.
*  **loop_re_eval.sh** - running `re_eval.py` on all 'Output_' directories inside a directory.
*  **collect_metrics.sh** - script looping over report files in muliple 'Output_' directories to collect metrics in one file.

