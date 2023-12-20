import re
import pandas as pd
import argparse

# The utterance has the following format:
# "<text>"
# This code will return <text> + whitespace
# or an empty string if there is no text (len(<text>) == 0)
#
# !!! This function is where you can add additional normalization
def process_utterance(utter):
  if utter[0] != '"':
    return ''
  # If the utterance is empty
  if utter[1] == '"':
    return ''
  else:
    return utter[1:len(utter)-2] + ' '
  
# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional arguments
parser.add_argument('--metafile', help = 'path to the .xls metadata file containing the list of .ort/TextGrid files',
                    default='C:/data/JASMIN_corpus/data/meta/xls/nl/speech_proc_rec.xls')
parser.add_argument('--indir', help = 'path to the .ort/TextGrid files directory',
                    default='C:/data/JASMIN_corpus/data/annot/text/ort/comp-q/nl/')
parser.add_argument('--outdir', help = 'path to the .txt output files directory', 
                    default='C:/data/speech_proc_test/')

# Read arguments from command line
args = parser.parse_args()

# Read the metadata file to get the list of files to be converted
df_nl = pd.DataFrame(pd.read_excel(args.metafile))
print('Metafile read. Converting files...')

# This code follows the TextGrid format of the Jasmin corpus
# Slight adjustments might need to be made for CGN
for i, j in df_nl.iterrows():
  # Change 'Root' to 'recordingID' iff you use CGN instead of Jasmin
  file = open(args.indir + j["Root"] + '.ort', encoding = "latin_1")
  out = open(args.outdir + j["Root"] + '.txt', 'w', encoding = "utf-8")

  lines = file.readlines()
  id_spk = False
  count = 0

  for line in lines:
    # We need to first find the ID of the speaker since the actual content
    # starts from there
    if re.match(r'"N0|"N1', line):
      id_spk = True
      continue
    # If we have not encountered the speaker ID yet, keep reading lines
    if not id_spk:
      continue
    # Once we found the speaker ID, we start processing the lines
    else:
      # IntervalTier or TextTier indicate that we have reached the end of the transcription
      # Therefore, we stop processing and save the output
      if line[1:len(line)-2] == "IntervalTier" or line[1:len(line)-2] == "TextTier":
        break
      # The format of each utterance of Jasmin is:
      # <start_time>
      # <end_time>
      # "<text>"
      #
      # We are interested in only the 3rd line (the text)
      if count < 2:
        count += 1
        continue
      processed_utter = process_utterance(line)
      out.write(processed_utter)
      count = 0
  
  file.close()
  out.close()

print('Conversion successful')
