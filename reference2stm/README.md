# Dataset files preprocessing
## Description
This folder contains script that preprocess the reference files used during evaluation. They either convert the reference files to STM format (`jasmin2stm.py`) or segment the audio files of the datasets (`segment_nbest.ipynb`).
## `jasmin2stm.py`
This script converts files in ORT format of the JASMIN corpus transcriptions to files in STM format accepted by sclite. There are some optional arguments:
- `-corpus_path`: The absolute/local path to the JASMIN corpus (the directory structure inside the corpus folder should be identical to the format mentioned in the corpus' documentation)
- `-out_path`: The absolute/local path to the output directory. Its structure must be the following:
```
output_dir
├───comp-p
│   ├───nl
│   └───vl
└───comp-q
    ├───nl
    └───vl
```
- `-vl`: Use it if you want to convert the Flemish part of JASMIN instead of the Dutch one

For HMI speech, the machine utterances are ignored.
## `segment_nbest.ipynb`
This Jupyter Notebook segments the audio and STM files of the N-Best 2008 Evaluation corpus. It contains code that deals with the Dutch subsets of the corpus, but changes can be easily made to accommodate the Flemish subsets. For more information about how it works, check out the notebook itself.

## `silence_jasmin.ipynb`
This Jupyter Notebook takes the first channel (corresponding to the human speaker) in Jasmin HMI speech recordings and silences the gaps inbetween the human-spoken segments. Important to notice is that the gaps inbetween the human segments are annotated using `inter_segment_gap` as an identifier. This identifier is used when applying silence. The audio is silenced using pydub's `AudioSegment.silent()`. For more details, read the notebook.