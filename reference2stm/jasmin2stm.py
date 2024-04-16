import re
import pandas as pd
import argparse


def process_utterance(utter, file_id, spk_id):
    res = file_id + ' 1 '
    # The first element is the # of utterances
    # A comment with spk_id will be added instead
    if utter[2][0] != '"':
        return ';;' + spk_id + '\n'
    # If there is no word spoken, add it as speech from speaker 'inter_segment_gap'
    if utter[2][1] == '"':
        res += 'inter_segment_gap ' + utter[0][0:len(utter[0])-1] + ' ' + utter[1][0:len(utter[1])-1] + ' <o,f0,>'
    else:
        # Text normalization (removing annotations such as *x, *v,
        text = re.sub(r'\*.', '', utter[2][1:len(utter[2])-2])
        # as well as ggg which denotes non-speech sounds made by the speaker
        text = re.sub('ggg', '', text)
        # and Xxx/xxx which denote words not understood by the human transcribers)
        text = re.sub('xxx', '', text)
        text = re.sub('Xxx', '', text)
        # If, after normalization, the text is empty, add it as speech from speaker 'inter_segment_gap'
        if text == '\n':
            res += 'inter_segment_gap ' + utter[0][0:len(utter[0])-1] + ' ' + utter[1][0:len(utter[1])-1] + ' <o,f0,>'
        else:
            # Else, add the utterance as speech from speaker <spk_id>
            res += spk_id + ' ' + utter[0][0:len(utter[0])-1] + ' ' + utter[1][0:len(utter[1])-1] + ' <o,f1,unknown> ' + text

    # Return the line in STM format followed by a newline character
    return res + '\n'


# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional arguments
parser.add_argument('-corpus_path', help='path to the JASMIN corpus',
                    default='C:/data/JASMIN_corpus/')
parser.add_argument('-out_path', help='path to the STM output files directory',
                    default='./whisper2ctm/output_dir/')
parser.add_argument('-vl', action='store_true',
                    help='Use it to convert the Flemish part of JASMIN instead of the Dutch part')

# Read arguments from command line
args = parser.parse_args()

country = 'nl'

if args.vl:
    country = 'vl'

# Read the "recordings.xls" metadata file for the Dutch/Flemish part of JASMIN
df = pd.DataFrame(pd.read_excel(args.corpus_path + 'data/meta/xls/' + country + '/recordings.xls'))

# Go through the rows of "recordings.xls" (which contains the metadata of all the recordings in the corpus
# for either Dutch or Flemish)
for i, j in df.iterrows():
    # Read the ORT file corresponding to the current row
    # j["Component"] corresponds to comp-p (HMI) or comp-q (read speech)
    # j["Root"] corresponds to file name
    file = open(args.corpus_path + 'data/annot/text/ort/' + j["Component"] + '/' + country
                + '/' + j["Root"] + '.ort', encoding="latin_1")
    # Open the output file corresponding to the input file in the output folder defined as arg
    out = open(args.out_path + j["Component"] + '/' + country
               + '/' + j["Root"] + '.stm', 'w', encoding="utf-8")
    lines = file.readlines()
    id_spk = ''

    count = 0
    utter = []
    for line in lines:
        # There is a lot of metadata in the ORT files that are of no interest
        # The actual transcription starts once the speaker ID is found
        # which starts with "N0 or "N1 (or "V000 for Flemish)
        if re.match(r'"N0|"N1|"V000', line):
            # Once found, set id_spk, without ""
            id_spk = line[1:len(line)-2]
            continue
        # If the speaker ID has not been found yet, keep going through the ORT file
        if id_spk == '':
            continue
        else:
            # "IntervalTier" or "TextTier" mark the end of the transcription
            if line[1:len(line)-2] == "IntervalTier" or line[1:len(line)-2] == "TextTier":
                break
            # The ORT format is
            #
            # start_time
            # end_time
            # "utterance"
            #
            # Save the start_time, end_time, and "utterance", then process everything
            if len(utter) < 3:
                utter.append(line)
                count += 1
                continue
            # If start_time, end_time, and "utterance" have been stored in the list,
            # start processing the utterance
            else:
                # Function is described above, returns a one line string followed by
                # a newline character
                processed_utter = process_utterance(utter, j["Root"], j["SpeakerID"])
                out.write(processed_utter)
                # Reset the list for the next utterance by adding the start_time of
                # the next utterance
                utter = [line]
                count = 1
                continue

    file.close()
    out.close()
