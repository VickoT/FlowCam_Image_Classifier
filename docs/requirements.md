# Requirements for FlowCam Image Classifier

Requirement ID | Requirement description                                             | Acceptance criteria              | Test cases
---------------|----------------------------------------------------------------------|----------------------------------|------------------------------------------------------------
R1             | Read a `.csv` metadata file correctly                                | Passes test                      | Function `read_metadata(path)` returns a DataFrame
R1.1           | File must exist and be readable                                      | Raises helpful error if not found| Missing file error includes path
R1.2           | Output must have expected columns                                    | Passes test                      | Column names match known structure
R1.3           | Output must have valid content                                       | Passes test                      | Example row content matches input
R1.4           | File is read within reasonable time                                  | Passes performance test          | File loads in under 1 second (small test file)

R2             | Extract subimages from collage image files                           | Passes test                      | Output folder contains cropped `.png` files
R2.1           | `.lst` metadata correctly maps to collage file                       | Passes test                      | Collage exists for each referenced entry
R2.2           | Cropping coordinates are correctly applied                           | Passes test                      | Output image size matches metadata

R3             | Classifier predicts image category                                   | Passes test                      | Each image classified as `Protist`, `Junk`, or `Missed`
R3.1           | Model loads from `.pkl`                                              | No error loading model           | `joblib.load(path_model)` works
R3.2           | Required features exist in `.csv`                                    | Passes test                      | All expected feature columns are present
R3.3           | Predictions are stored in DataFrame                                  | Passes test                      | `df['Predictions']` column exists
R3.4           | Images are moved to correct category folders                         | Passes test                      | Files appear in correct destination folder

R4             | Generate a report summarizing classification results                 | Report file created              | `report.txt` exists in output directory
R4.1           | Report includes protist concentration estimate                       | Passes calculation test          | Output contains `protists/ml`
R4.2           | Report includes counts per class                                     | Passes test                      | Junk, Missed, Protist counts included

R5             | Clear, helpful error messages                                        | Error output is user friendly    | Missing input or model triggers descriptive messages

R6             | Batch mode: can process multiple runs                                | All subfolders processed         | Each valid subdirectory generates its own output
R6.1           | Output folders are created per sample                                | Output folders exist             | `Output_<sample_name>` exists for each run
R6.2           | Combined report summarizes all runs                                  | Combined file created            | `summary_report.tsv` contains counts from each sample
R6.3           | Fails gracefully if one run is broken                                | Continues other runs             | Broken subfolder is skipped with warning

R7             | Modular structure using OOP                                          | Code uses reusable components    | Key paths and logic wrapped in classes (`PathConfig`, `SampleProcessor`)
R7.1           | Script can be reused as a library                                    | Functions callable independently | Refactored functions can be imported and tested

R8             | Code is tested                                                       | Tests exist and pass             | Use `pytest` or `unittest` for core functions
R8.1           | At least metadata reading is tested                                  | Tests implemented                | `tests/test_read_metadata.py` exists
R8.2           | Image classification tested on dummy data                            | Tests implemented                | Model is tested on small mock `.csv`

R100           | Follows best practices in scientific software                        | All team members agree           | Code is versioned, documented, and structured
R100.1         | Requirements are documented and used to track progress               | Used to create GitHub issues     | Each `R#` item maps to a GitHub issue
R100.2         | Contributions are tracked                                             | Git history shows authorship     | Forked structure allows individual credit
