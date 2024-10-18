# Notebooks for running the ASR models
## Description
This folder contains the Jupyter notebooks used for running the different models to generate transcriptions. These transcriptions would then be used as the hypothesis files when calculating the WER and alignments.

## Models evaluated
The models that have been evaluated are the following:
- [Kaldi_NL](https://github.com/opensource-spraakherkenning-nl/Kaldi_NL) - the `radboud_OH` version was used; not present in this folder because a Docker version of it has been used locally
- [whisper_timestamped](https://github.com/linto-ai/whisper-timestamped) - this version was used instead of the original implementation from OpenAI due to the fact that, at the time of starting this benchmark, timestamps at a word level were not available, which is a requirement for running the tool that computes WER and alignments. File: `whisper_timestamped_benchmark.ipynb`
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper/) - best-performing from the initial benchmark. File: `faster_whisper_benchmark.ipynb`
- [XLS-R fine-tuned on Dutch](https://huggingface.co/jonatasgrosman/wav2vec2-xls-r-1b-dutch)
- Massively Multilingual Speech (MMS):
    - pre-trained on 1162 languages: https://huggingface.co/facebook/mms-1b-all
    - pre-trained on 102 languages (of Fleurs dataset): https://huggingface.co/facebook/mms-1b-fl102

XLS-R and MMS use the same script file (`xlsr_mms_benchmark.ipynb`)

For more information about a specific model, check the comments in the respective notebook.