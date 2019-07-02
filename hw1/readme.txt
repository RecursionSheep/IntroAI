src\pinyin.py 是三元模型的代码，src\pinyin2.py 是二元模型的代码。
bin\pinyin.exe 是三元模型的可执行文件，bin\pinyin2.exe 是二元模型的可执行文件。
data\char.txt, data\freq_one.txt, data\freq_two.txt, data\freq_three.txt, data\pinyin.txt 是程序运行必须的数据文件。
data\input.txt, data\answer.txt 是测试的输入和输出。

运行方式：
pinyin .\..\data\input.txt .\..\data\output.txt
或
python pinyin.py .\..\data\input.txt .\..\data\output.txt
