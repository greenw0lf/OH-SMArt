import argparse
import os

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional arguments
parser.add_argument('-in', '--input', help = 'path to the CTM input files directory',
                    default='input_dir')
parser.add_argument('-out', '--output', help = 'path to the TXT output files directory', 
                    default='output_dir')

# Read arguments from command line
args = parser.parse_args()

# Iterate through the contents of the input folder
for file in os.listdir(args.input):
    # If it's not a file, skip
    if not os.path.isfile(os.path.join(args.input, file)):
        continue
    # Split the string using .ctm as a separator
    split_on_ctm = file.split('.ctm')
    # If the filename does not end in .ctm, skip
    if len(split_on_ctm) < 2:
        continue

    # Get the filename without .ctm
    filename = split_on_ctm[0]
    # Create the TXT output file (using the name of the input file)
    out = open(os.path.join(args.output, filename + '.txt'), 'w', encoding = "utf-8")

    with open(args.input + file, encoding='utf-8') as inp:
        for line in inp.readlines():
            segments = line.split(' ')
            out.write(segments[4])
            out.write('\n')
    
    out.close()
