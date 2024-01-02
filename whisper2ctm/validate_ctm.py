import argparse
import json
import os

# Initialize parser
parser = argparse.ArgumentParser()


parser.add_argument('-in', '--input', help = 'path to the CTM files directory',
                    default='input_dir/')
 
# Read arguments from command line
args = parser.parse_args()

# Iterate through the contents of the input folder
for file in os.listdir(args.input):
    # If it's not a file, skip
    if not os.path.isfile(os.path.join(args.input, file)):
        continue
    # Split the string using .ctm as a separator
    split_on_json = file.split('.ctm')
    # If the filename does not end in .ctm, skip
    if len(split_on_json) < 2:
        continue

    with open(args.input + file, encoding='utf-8') as file_to_val:
        lines = file_to_val.readlines()

        i = 0
        for line in lines:
            # Keep track of line we are at in current file
            i += 1
            segments = line.split(' ')
            # The CTM expected as input for sclite has 6 parts
            # If it doesn't have 6 parts, then something went wrong (and the evaluation
            # will also fail)
            if len(segments) != 6:
                print('Irregularity detected\nFile: ' + file + '\nLine: ' + str(i))

print('\nValidation complete')