# Whisper output to CTM
## Description
This is a simple tool that I created for converting the output of [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped) to the format required by the [ASR-NL-benchmark](https://github.com/opensource-spraakherkenning-nl/ASR_NL_benchmark) tool.

## Setup & Example run
Simply clone the repo locally, then use your preferred type of terminal and navigate to the local repo directory. From there, you can run:

`python main.py`

which will use the example files as input/output.

## Input format: JSON
The input format is a JavaScript Object Notation (JSON) file. It represents the output of `whisper-timestamped`, whose format you can find [here](https://github.com/linto-ai/whisper-timestamped#example-output). An example input file (`input_dir/example_in.json`) is also provided with this repo.

The part that is important to convert is the `words` underneath each element of `segments`. A `word` contains the following information:
- `text`: the word transcribed by Whisper
- `start`: the start of the timestamp
- `end`: the end of the timestamp
- `confidence`: the confidence score that the model has for the outputted word

All of the keys of a `word` will be used when generating our output CTM file (see below).

## Output format: CTM
The output format is called a Time Marked Conversation file. More information about it can be found [here](https://github.com/opensource-spraakherkenning-nl/ASR_NL_benchmark/tree/main#ctm-format). An example output file (`output_dir/example_out.ctm`) is also provided with this repo.

A very brief summary is that it is a file made up of multiple lines, each line having a timestamped word. The format of a line is:

    File_id Channel Begin_time Duration Word Confidence

You can add comments by adding ';;' at the start of the line.

Example:

```
;; Some information you want to comment out like a description
;; More information you want to include and comment out
Your_favorite_tv_show_2021_S1_E1 A 0.000 0.482 The 0.95
Your_favorite_tv_show_2021_S1_E1 A 0.496 0.281 first 0.98
Your_favorite_tv_show_2021_S1_E1 A 1.216 0.311 line 0.88
```

## Advanced run using arguments
The tool itself would be useless if you cannot use your own files or format the output as you wish. Therefore, 3 arguments have been added for convenience:
- `-in/--input`: Should correspond to the absolute/local path to the directory where the input JSON files can be found
- `-out/--output`: Should correspond to the absolute/local path to the directory where the output CTM files can be created
- `--stereo`: An optional flag that should be used if a stereo audio file has been transcribed and 2 transcriptions have been generated for that audio file, 1 per channel
- `--jasmin`: An optional flag that can be used when the alignments need to be readjusted (based on initial results obtained for Whisper on the Jasmin corpus, hence the name)

When it comes to the CTM output for each JSON input, it will use as `File_id` the JSON filename without the .json extension, and the `Channel` is set to 1 by default (for stereo, it uses the **last character** before the .json extension to determine the channel)

Future plans might include customizing these 2 settings, but for now they will stay this way.

## More information about the `--stereo` and `--jasmin` arguments
The filename format expected when using the `--stereo` argument is `{File_id}-{1/2}.json`, where `File_id` is the same as the one mentioned in the subsection above and `{1/2}` refers to the channel that has been transcribed.

You can run it on the examples provided as so:

```python main.py -in stereo_input -out stereo_output --stereo```
<br><br><br>
As for the `--jasmin` flag, the issue I faced with Jasmin and Whisper is that the first word of a segment in the reference file would be considered as a deletion and the same word in the hypothesis file was an insertion. This was because the alignment algorithm used for Whisper or the alignments of the Jasmin reference files were not accurate. This flag will realign the first word of each segment such that it starts at the predicted end time minus 0.1 seconds. This heavily reduced the number of insertions and deletions and, thus, the WER was lower.

To be more specific, the new `start` of the first word in each segment in the hypothesis file becomes `end - 0.1`.

## Useful tool: `validate_ctm.py`
In some cases, I encountered errors with the output given by Whisper. The particular error that this tool detects is when there is more than one word per line. For example:

    filename 1 16.61 0.46 Beeld & 0.89

The tool simply checks if there are 6 separate strings separated by space on each line (if it meets the format requirement as described in the section above).

The command to run is:

```python validate_ctm.py -in path/to/ctm/files/folder```

Replace `path/to/ctm/files/folder` with the path where the CTM files to be validated can be found.

## Another useful tool: `ctm2txt.py`
This code takes a word-level timestamped CTM file and converts it to a TXT file, with all the words concatenated on one line and without any timestamps or other information. I used this code to compare the outputs of `whisper-timestamped` and `faster-whisper` to see in more detail whether the timestamping created the difference in WER performance or if the transcriptions are also substantially different.

## Converting Huggingface Whisper output to CTM: `hf2ctm.py`

### Format of Huggingface output (JSON)

The output has the following format:

```
{
    "words": [
        {
            "text": "So,",
            "timestamp": [
                0,
                0.8
            ]
        },
        {
            "text": "let's",
            "timestamp": [
                0.8,
                1.4
            ],
        },
        ...
    ]
}
```

### Arguments

Similar arguments as for the `main.py` file are used:
- `-in/--input`: Should correspond to the absolute/local path to the directory where the input JSON files can be found
- `-out/--output`: Should correspond to the absolute/local path to the directory where the output CTM files can be created

## Acknowledgements
- [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped): Whisper Speech Recognition using word-level timestamps and confidence (License GPL v3)
- [ASR-NL-benchmark](https://github.com/opensource-spraakherkenning-nl/ASR_NL_benchmark): ASR benchmark tool for the Dutch language (License MIT)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper): Faster and memory-efficient implementation of Whisper (License MIT)
