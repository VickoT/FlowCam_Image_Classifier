# FlowCam Image Classifier - Functional Requirements

Version: 0.1
Last updated: 2025-05-23

Req ID      | Requirements description                                                
------------|-------------------------------------------------------------------------
R1          | Input handling                                                    
R1.1        | Raw input data is located                                         
R1.1.1      | The .tif files shall be located and read                              
R1.1.2      | The .lst files shall be located and read                        
R1.1.3      | The .summary files shall be located and read
R1.2        | The .tif file image collages shall be separated into individual images
R2          | Environment setup
R2.1        | Working paths shall be defined and resolved
R2.2        | Required directories shall be created 
R2.2.1      | The output directory shall be created at default or specified location
R3          | Images are classified                                       
R3.1        | All images shall be classified
R3.2        | The images shall be moved into corresponding category folder
R4          | Report file is generated
R4.1        | The report file shall read volume data from the `*_summary.csv` file
R4.2        | The report shall include the number of images in each category
R4.3        | The report shall include the calculated protist concentration