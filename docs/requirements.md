# Requirements for FlowCam Image Classifier

Requirement ID | Requirement description                                             | Acceptance criteria             | Test cases
---------------|----------------------------------------------------------------------|----------------------------------|---------------------------
**R1** | The program reads and parses `.tif` image files and associated `.csv` metadata files. | Returns valid table             | Function returns a DataFrame with correct columns
**R2** | The program extracts images from `.tif` collage files using metadata from `.lst`. | Passes test  | Output directory contains expected number of cropped `.png` images
**R3** | The program classifies the extracted images using a pretrained model. | Passes test  | Classified images appear in folders: `Junk`, `Missed`, `Protist`
**R4** | The program generates a report summarizing classification results.| `report.txt` is created | Output file contains sample name, counts, and estimated protist/mL
**R5** | The program handles common errors gracefully. | Helpful error messages are shown| Missing file or broken input yields descriptive message.
**R6** | The program can handle batch input. | Program processes all valid FlowCam output subdirectories in the given parent directory. | Each subdirectory is processed, and individual output folders and reports are created.