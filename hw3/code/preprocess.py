import os
import re

fin = open(r'.\vec\sgns.sogounews.bigram-char', 'r', encoding = 'utf-8')
text = fin.readline()
num, dim = int(text.split()[0]), int(text.split()[1])
dict = {}
for i in range(num):
	text = fin.readline()
	dict[text.split(' ')[0]] = i + 1
fin.close()

fin = open(r'.\data\sinanews.demo', 'r', encoding = 'utf-8')
fout1 = open(r'.\data\demo.text', 'w', encoding = 'utf-8')
fout2 = open(r'.\data\demo.label', 'w', encoding = 'utf-8')

while True:
	text = fin.readline()
	if not text:
		break
	words = text.split()
	label = 0
	max_num = -1
	n = len(words)
	for i in range(n):
		if (i >= 2) and (i <= 9):
			k = int(re.findall('\d+', words[i])[0])
			if k > max_num:
				max_num = k
				label = i - 2
		if (i > 9):
			if (i > 10):
				fout1.write(' ')
			if words[i] in dict:
				fout1.write(str(dict[words[i]]))
			else:
				fout1.write('0')
	fout1.write('\n')
	fout2.write(str(label) + '\n')
fin.close()
fout1.close()
fout2.close()

fin = open(r'.\data\sinanews.train', 'r', encoding = 'utf-8')
fout1 = open(r'.\data\train.text', 'w', encoding = 'utf-8')
fout2 = open(r'.\data\train.label', 'w', encoding = 'utf-8')

while True:
	text = fin.readline()
	if not text:
		break
	words = text.split()
	n = len(words)
	label = 0
	max_num = -1
	for i in range(n):
		if (i >= 2) and (i <= 9):
			k = int(re.findall('\d+', words[i])[0])
			if k > max_num:
				max_num = k
				label = i - 2
		if (i > 9):
			if (i > 10):
				fout1.write(' ')
			if words[i] in dict:
				fout1.write(str(dict[words[i]]))
			else:
				fout1.write('0')
	fout1.write('\n')
	fout2.write(str(label) + '\n')
fin.close()
fout1.close()
fout2.close()

fin = open(r'.\data\sinanews.test', 'r', encoding = 'utf-8')
fout1 = open(r'.\data\test.text', 'w', encoding = 'utf-8')
fout2 = open(r'.\data\test.label', 'w', encoding = 'utf-8')

while True:
	text = fin.readline()
	if not text:
		break
	words = text.split()
	n = len(words)
	label = 0
	max_num = -1
	for i in range(n):
		if (i >= 2) and (i <= 9):
			k = int(re.findall('\d+', words[i])[0])
			if k > max_num:
				max_num = k
				label = i - 2
		if (i > 9):
			if (i > 10):
				fout1.write(' ')
			if words[i] in dict:
				fout1.write(str(dict[words[i]]))
			else:
				fout1.write('0')
	fout1.write('\n')
	fout2.write(str(label) + '\n')
fin.close()
fout1.close()
fout2.close()
