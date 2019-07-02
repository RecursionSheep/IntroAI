fin1 = open(r'.\..\data\answer.txt', 'r', encoding = 'utf-8')
fin2 = open(r'.\..\data\output.txt', 'r', encoding = 'utf-8')

score = 0
for i in range(1000):
	text1 = fin1.readline()
	text2 = fin2.readline()
	if text1 == text2:
		score += 1
print(score / 1000)
