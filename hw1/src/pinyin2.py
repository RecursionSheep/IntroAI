import os
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

eps = 1000

ch_list = []
freq_one = {}
fin = open(r'.\..\data\char.txt', 'r', encoding = 'utf-8')
text = fin.readline()
for ch in text:
	ch_list.append(ch)
	freq_one[ch] = 0

fin = open(r'.\..\data\freq_one.txt', 'r', encoding = 'utf-8')
while True:
	text = fin.readline()
	if text == None:
		break
	word_list = text.split()
	if len(word_list) == 0:
		break
	freq_one[word_list[0]] = int(word_list[1])
	
pinyin_dict = {}
fin = open(r'.\..\data\pinyin.txt', 'r', encoding = 'utf-8')
while True:
	text = fin.readline()
	if text == None:
		break
	word_list = text.split()
	if len(word_list) == 0:
		break
	pinyin = word_list[0]
	pinyin_dict[pinyin] = []
	num = len(word_list)
	for i in range(1, num):
		if (not word_list[i] in freq_one) or (freq_one[word_list[i]] < 10):
			continue
		pinyin_dict[pinyin].append(word_list[i])

freq_two = {}
fin = open(r'.\..\data\freq_two.txt', 'r', encoding = 'utf-8')
while True:
	text = fin.readline()
	if text == None:
		break
	word_list = text.split()
	if len(word_list) == 0:
		break
	freq_two[word_list[0], word_list[1]] = int(word_list[2])

fin = open(input_file, 'r', encoding = 'utf-8')
fout = open(output_file, 'w', encoding = 'utf-8')
while True:
	prob = {}
	pre = {}
	text = fin.readline()
	if text == None:
		break
	word_list = text.split()
	if len(word_list) == 0:
		break
	word = word_list[0]
	cnt = 0
	n = len(word_list)
	for ch in pinyin_dict[word]:
		cnt += freq_one[ch] + eps
	for ch in pinyin_dict[word]:
		prob[0, ch] = 1.0 * (freq_one[ch] + eps) / cnt
	for id in range(1, n):
		last_word = word_list[id - 1]
		word = word_list[id]
		for ch in pinyin_dict[word]:
			prob[id, ch] = 0
			pre[id, ch] = 0
		for last_ch in pinyin_dict[last_word]:
			cnt = 0
			for ch in pinyin_dict[word]:
				if (last_ch, ch) in freq_two:
					cnt += freq_two[last_ch, ch] + eps
				else:
					cnt += eps
			for ch in pinyin_dict[word]:
				if (last_ch, ch) in freq_two:					
					trans_prob = 1.0 * (freq_two[last_ch, ch] + eps) / cnt
				else:
					trans_prob = 1.0 * eps / cnt
				if prob[id - 1, last_ch] * trans_prob > prob[id, ch]:
					prob[id, ch] = prob[id - 1, last_ch] * trans_prob
					pre[id, ch] = last_ch
	last_word = word_list[n - 1]
	ans = []
	max_prob = 0
	for ch in pinyin_dict[last_word]:
		if prob[n - 1, ch] > max_prob:
			max_prob = prob[n - 1, ch]
			last_ch = ch
	for id in range(n - 1, 0, -1):
		ans.append(last_ch)
		last_ch = pre[id, last_ch]
	ans.append(last_ch)
	for id in range(n - 1, -1, -1):
		fout.write(ans[id])
	fout.write('\n')
