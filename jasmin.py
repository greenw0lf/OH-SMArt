import re
import pandas as pd


def process_utterance(utter, file_id, spk_id):
  res = file_id + ' 1 '
  if utter[2][0] != '"':
    return ';;' + spk_id + '\n'
  if utter[2][1] == '"':
    res += 'inter_segment_gap ' + utter[0][0:len(utter[0])-2] + ' ' + utter[1][0:len(utter[1])-2] + ' <o,f0,>'
  else:
    text = re.sub(r'\*.', '', utter[2][1:len(utter[2])-2])
    text = re.sub('ggg', '', text)
    text = re.sub('xxx', '', text)
    text = re.sub('Xxx', '', text)
    if text == '\n':
      res += 'inter_segment_gap ' + utter[0][0:len(utter[0])-2] + ' ' + utter[1][0:len(utter[1])-2] + ' <o,f0,>'
    else:
      res += spk_id + ' ' + utter[0][0:len(utter[0])-2] + ' ' + utter[1][0:len(utter[1])-2] + ' <o,f1,unknown> ' + text
  
  return res + '\n'


df_nl = pd.DataFrame(pd.read_excel('C:/data/JASMIN_corpus/data/meta/xls/nl/recordings.xls'))
# df_vl = pd.DataFrame(pd.read_excel('C:/data/JASMIN_corpus/data/meta/xls/vl/recordings.xls'))

for i, j in df_nl.iterrows():
  file = open('C:/data/JASMIN_corpus/data/annot/text/ort/' + j["Component"] + '/nl/' \
               + j["Root"] + '.ort', encoding = "latin_1")
  out = open('C:/data/JASMIN_corpus/data/annot/text/ort/' + j["Component"] + '/nl/' \
               + j["Root"] + '.stm', 'w', encoding = "utf-8")
  lines = file.readlines()
  id_spk = ''

  count = 0
  utter = []
  for line in lines:
    if re.match(r'"N0|"N1', line):
      id_spk = line[1:len(line)-2]
      utter = []
      continue
    if id_spk == '':
      continue
    else:
      if  line[1:len(line)-2] == "IntervalTier" or line[1:len(line)-2] == "TextTier":
        break
      if len(utter) < 3:
        utter.append(line)
        count += 1
        continue
      else:
        processed_utter = process_utterance(utter, j["Root"], j["SpeakerID"])
        out.write(processed_utter)
        utter = [line]
        count = 1
        continue
  
  file.close()
  out.close()
