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
    for word in obj['words']:
        # If there are no words transcribed by Whisper
        if word['text'] == '':
            continue
        # Access the list of words from the segment
        # 'timestamp' is an array containing the start time as the first element
        # and the end time as the second one
        string = filename + ' 1 ' + str(round(word['timestamp'][0], 2)) \
            + ' ' + str(round(word['timestamp'][1] - word['timestamp'][0], 2)) + ' ' \
                + word['text'].strip() + ' 0'
        out.write(string)
        out.write('\n')
    # Close both files
    inp.close()
    out.close()
