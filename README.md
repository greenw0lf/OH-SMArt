# OH-SMArt
Code related to the work done at University of Twente on the OH-SMArt project.

Results can be found here: https://opensource-spraakherkenning-nl.github.io/ASR_NL_results/ (under `UT's benchmark`)

## Repo structure

- `evaluation` - contains the code for running the evaluated models. For more details, check out the README inside the folder
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

## Files used to compute the results
The hypothesis, reference, WER score + alignment files can be found in the `tar.gz` here: https://surfdrive.surf.nl/files/index.php/f/15685340255

The top-level structure is represented by the 3 datasets that have been investigated:
- Common Voice (CV)
- Jasmin-CGN
- N-Best 2008 Eval. Corpus

The bottom level of each dataset contains the following:
- `hyp` folder - contains the hypothesis files (output) of each model, in CTM format
- `wer_alignments` folder - contains 2 files for each model:
    - `.dtl` - performance metrics (WER, SER, % insertions, deletions, substitutions, confusion pairs)
    - `.prf` - alignments of hypothesis and reference sentences
- `reference.stm` - contains the reference file for the specific dataset/subset, in STM format

For more information about the `CTM` or `STM` formats of the hypothesis and reference respectively, check out [this repository](https://github.com/opensource-spraakherkenning-nl/ASR_NL_benchmark).

### Jasmin-CGN

**Jasmin-CGN** has the following structure:
- `NL/VL` - Netherlands Dutch/Flemish
    - `comp_p/comp_q` - Conversational (HMI)/Read speech
        - `1-5` representing each speaker group:
            1. Native children
            2. Native teenagers
            3. Non-native children
            4. Non-native adults
            5. Native elderly

For more information about the metadata of this dataset, I recommend checking out the documentation of the dataset itself.

### N-Best 2008

**N-Best** has the following structure:
- `bn_nl` - Broadcast News in the Netherlands
- `bn_vl` - Broadcast News in Belgium
- `cts_nl` - Conversational Telephone Speech in the Netherlands
- `cts_vl` - Conversational Telephone Speech in Belgium

## Whisper benchmarking

Additional benchmarking of various Whisper implementations has been done.

- Results: https://opensource-spraakherkenning-nl.github.io/ASR_NL_results/ (under `NISV's Whisper benchmark`)
- Jupyter Notebooks: https://github.com/greenw0lf/whisper-benchmark
