# OH-SMArt
Code related to the work done at University of Twente on the OH-SMArt project.

## Repo structure

- `evaluation` - contains the code that runs Whisper on audio to generate transcriptions
- `whisper2ctm` - contains the code that converts the output of Whisper to the CTM file format required by sclite. For more details, check out the README inside the folder
- `reference2stm` - contains the code used for processing the reference files of the datasets used in evaluation. For more details, check out the README inside the folder
- `merge_files.py` - a helper script that merges text-like files into one (also works with CTM and STM formats)

## Requirements
- Python 3.x.x (I tested using Python version 3.11.6 but older/newer versions should also be working just as fine)

## `merge_files.py`
A tool to merge files of the same extension into one file. There are some optional arguments:
- `-in/--input`: Should correspond to the absolute/local path to the directory where the files to be merged can be found
- `-out/--output`: Should correspond to the absolute/local path + filename of the merged file to be generated
- `--file_ext`: The extension of the files to be merged. Default is `ctm`

Examples can be found in the code. It is required to have all the files to be merged into one directory.
