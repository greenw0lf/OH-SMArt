import argparse
import json
import os

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional arguments
parser.add_argument('-in', '--input', help = 'path to the JSON input files directory',
                    default='input_dir')
parser.add_argument('-out', '--output', help = 'path to the CTM output files directory', 
                    default='output_dir')
parser.add_argument('--stereo', action = 'store_true', 
                    help = 'use the flag if the transcribed audio is stereo (2 channels)')
parser.add_argument('--jasmin', action = 'store_true',
                    help = "use the flag to realign the first word of each segment (for Jasmin \
                        corpus evaluation)")
 
# Read arguments from command line
args = parser.parse_args()

# Iterate through the contents of the input folder
for file in os.listdir(args.input):
    # If it's not a file, skip
    if not os.path.isfile(os.path.join(args.input, file)):
        continue
    # Split the string using .json as a separator
    split_on_json = file.split('.json')
    # If the filename does not end in .json, skip
    if len(split_on_json) < 2:
        continue
    # Get the filename without .json
    filename = split_on_json[0]
    # Open the JSON input file
    inp = open(os.path.join(args.input, file), encoding = "utf-8")
    # Create the CTM output file (using the name of the input file)
    out = open(os.path.join(args.output, filename + '.ctm'), 'w', encoding = "utf-8")
    # Read/Load the JSON content
    obj = json.load(inp)
    
    # Loop through the list of segments according to the JSON format of whisper-timestamped
    for segment in obj['segments']:
        # If there are no words transcribed by Whisper (this happened for one of the files
        # for Whisper v3 with VAD)
        if segment['text'] == '':
            continue
        # Access the list of words from the segment
        words = segment['words']
        # For Jasmin realign: we only want to realign the first word of a segment
        # The first word is always detected as an insertion by Whisper + deletion in the
        # reference file
        first_word = True
        # Loop through the words
        for word in words:
            if args.jasmin and first_word:
                word['start'] = word['end'] - 0.1
                first_word = False
            # Assumed stereo format is {name-of-file}-1.json (or {name-of-file}-2.json for the 2nd channel)
            if args.stereo:
                string = filename[:-2] + ' ' + filename[-1] + ' ' + str(round(word['start'], 2)) \
                + ' ' + str(round(word['end'] - word['start'], 2)) + ' ' \
                    + word['text'] + ' ' +  str(round(word['confidence'], 2))
            else:
                string = filename + ' 1 ' + str(round(word['start'], 2)) \
                    + ' ' + str(round(word['end'] - word['start'], 2)) + ' ' \
                        + word['text'] + ' ' +  str(round(word['confidence'], 2))
            out.write(string)
            out.write('\n')
    # Close both files
    inp.close()
    out.close()

