import argparse
import glob

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional arguments
parser.add_argument('-in', '--input', help = 'path to the files directory',
                    default='input_dir/')
parser.add_argument('-out', '--output', help = 'path + name of the merged file', 
                    default='output_dir/merged.ctm')
parser.add_argument('-file_ext', help = 'extension that files to be merged have (without the dot)',
                    default='ctm')

# Read arguments from command line
args = parser.parse_args()

read_files = glob.glob(args.input + "*." + args.file_ext)
with open(args.output, "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())

outfile.close()
