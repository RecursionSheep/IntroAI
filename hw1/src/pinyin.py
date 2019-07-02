import os
import sys
from decimal import *

input_file = sys.argv[1]
output_file = sys.argv[2]

eps = 1
eps2 = 1000
getcontext().prec = 25

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
		if (not word_list[i] in freq_one) or (freq_one[word_list[i]] < 100):
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

freq_three = {}
fin = open(r'.\..\data\freq_three.txt', 'r', encoding = 'utf-8')
while True:
	text = fin.readline()
	if text == None:
		break
	word_list = text.split()
	if len(word_list) == 0:
		break
	freq_three[word_list[0], word_list[1], word_list[2]] = int(word_list[3])

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
		cnt += freq_one[ch] + eps2
	max_prob = Decimal(0)
	max_word = None
	for ch in pinyin_dict[word]:
		prob[0, ch] = Decimal(freq_one[ch] + eps2) / Decimal(cnt)
		if (prob[0, ch] > max_prob):
			max_prob = prob[0, ch]
			max_word = ch
	if n == 1:
		fout.write(max_word)
		fout.write('\n')
		continue
	last_word = word
	id = 1
	word = word_list[id]
	for last_ch in pinyin_dict[last_word]:
		cnt = 0
		for ch in pinyin_dict[word]:
			prob[id, last_ch, ch] = 0
			if (last_ch, ch) in freq_two:
				cnt += freq_two[last_ch, ch] + eps2
			else:
				cnt += eps2
		for ch in pinyin_dict[word]:
			if (last_ch, ch) in freq_two:					
				trans_prob = Decimal(freq_two[last_ch, ch] + eps2) / Decimal(cnt)
			else:
				trans_prob = Decimal(eps2) / Decimal(cnt)
			prob[id, last_ch, ch] = trans_prob
	for id in range(2, n):
		last_word_2 = word_list[id - 2]
		last_word = word_list[id - 1]
		word = word_list[id]
		for last_ch in pinyin_dict[last_word]:
			for ch in pinyin_dict[word]:
				prob[id, last_ch, ch] = 0
				pre[id, last_ch, ch] = 0
		for last_ch_2 in pinyin_dict[last_word_2]:
			cnt = 0
			for ch in pinyin_dict[last_word_2]:
				if ch in freq_one:
					cnt += freq_one[ch] + eps2
				else:
					cnt += eps2
			ch_prob = Decimal(freq_one[last_ch_2]) / Decimal(cnt)
			for last_ch in pinyin_dict[last_word]:
				cnt = 0
				flag = False
				for ch in pinyin_dict[word]:
					if (last_ch_2, last_ch, ch) in freq_three:
						cnt += freq_three[last_ch_2, last_ch, ch] + eps
						flag = True
					else:
						cnt += eps
				if not flag:
					cnt = 0
					for ch in pinyin_dict[word]:
						if (last_ch, ch) in freq_two:
							cnt += freq_two[last_ch, ch] + eps2
						else:
							cnt += eps2
					for ch in pinyin_dict[word]:
						if (last_ch, ch) in freq_two:
							trans_prob = ch_prob * Decimal(freq_two[last_ch, ch] + eps2) / Decimal(cnt)
						else:
							trans_prob = ch_prob * Decimal(eps2) / Decimal(cnt)
						if prob[id - 1, last_ch_2, last_ch] * trans_prob > prob[id, last_ch, ch]:
							prob[id, last_ch, ch] = prob[id - 1, last_ch_2, last_ch] * trans_prob
							pre[id, last_ch, ch] = last_ch_2
					continue
				for ch in pinyin_dict[word]:
					if (last_ch_2, last_ch, ch) in freq_three:
						trans_prob = Decimal(freq_three[last_ch_2, last_ch, ch] + eps) / Decimal(cnt)
					else:
						trans_prob = Decimal(eps) / Decimal(cnt)
					if prob[id - 1, last_ch_2, last_ch] * trans_prob > prob[id, last_ch, ch]:
						prob[id, last_ch, ch] = prob[id - 1, last_ch_2, last_ch] * trans_prob
						pre[id, last_ch, ch] = last_ch_2
	last_word = word_list[n - 1]
	last_word_2 = word_list[n - 2]
	ans = []
	max_prob = Decimal(0)
	for ch in pinyin_dict[last_word]:
		for ch_2 in pinyin_dict[last_word_2]:
			if prob[n - 1, ch_2, ch] > max_prob:
				max_prob = prob[n - 1, ch_2, ch]
				last_ch = ch
				last_ch_2 = ch_2
	ans.append(last_ch)
	for id in range(n - 1, 1, -1):
		ans.append(last_ch_2)
		last_ch, last_ch_2 = last_ch_2, pre[id, last_ch_2, last_ch]
	ans.append(last_ch_2)
	for id in range(n - 1, -1, -1):
		fout.write(ans[id])
	fout.write('\n')
	prob.clear()
	pre.clear()
