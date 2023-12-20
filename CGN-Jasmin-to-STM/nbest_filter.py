import re

file = open("C:/data/nbest_eval/ref/nbest-eval-2008-bn-nl.stm", 'r')
out = open("C:/data/nbest_eval/ref/nbest-eval-2008-bn-nl-norm.stm", 'w')
ref = file.read()

ref = re.sub(r'\*.', '', ref)
ref = re.sub('ggg', '', ref)
ref = re.sub('xxx', '', ref)

out.write(ref)

file.close()
out.close()