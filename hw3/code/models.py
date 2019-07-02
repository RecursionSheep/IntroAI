import numpy as np
import scipy
import keras
import keras.backend as tf
from sklearn.metrics import f1_score

PAD_LENGTH = 800
CLASS_NUM = 8

def get_data(text_dir, label_dir):
	fin1 = open(text_dir, 'r')
	fin2 = open(label_dir, 'r')
	x, y = [], []
	while True:
		text = fin1.readline()
		if not text:
			break
		text = text.split()
		n = len(text)
		seq = np.zeros((PAD_LENGTH))
		for i in range(min(n, PAD_LENGTH)):
			seq[i] = int(text[i])
		x.append(seq)
		label = int(fin2.readline())
		y.append(label)
	return np.array(x), np.array(y)

class callback(keras.callbacks.Callback):
	def __init__(self, training_data, validation_data):
		self.x = training_data[0]
		self.y = training_data[1]
		self.x_val = validation_data[0]
		self.y_val = validation_data[1]
	
	def on_train_begin(self, logs = {}):
		return
 
	def on_train_end(self, logs = {}):
		return
 
	def on_epoch_begin(self, epoch, logs = {}):
		return
 
	def on_epoch_end(self, epoch, logs = {}):
		y_pred = self.model.predict(self.x)
		size = y_pred.shape[0]
		print('f-score: %s' % str(f1_score(np.argmax(self.y, axis = 1), np.argmax(y_pred, axis = 1), labels = range(8), average = 'macro')))
		ave = 0.
		for i in range(size):
			ave += scipy.stats.pearsonr(self.y[i], y_pred[i])[0]
		ave /= size;
		print('correl: %s' % str(ave))
		
		y_pred_val = self.model.predict(self.x_val)
		size = y_pred_val.shape[0]
		print('f-score val: %s' % str(f1_score(np.argmax(self.y_val, axis = 1), np.argmax(y_pred_val, axis = 1), labels = range(8), average = 'macro')))
		ave = 0.
		for i in range(size):
			ave += scipy.stats.pearsonr(self.y_val[i], y_pred_val[i])[0]
		ave /= size;
		print('correl val: %s' % str(ave))
		
		return
 
	def on_batch_begin(self, batch, logs = {}):
		return
 
	def on_batch_end(self, batch, logs = {}):
		return

def MLP_Model(input_shape, word_num, dim):
	x = keras.layers.Input(input_shape)
	y = keras.layers.Embedding(word_num + 1, dim, weights = [word_mat], input_length = PAD_LENGTH, trainable = False)(x)
	y = keras.layers.Flatten()(y)
	
	# low-rank decomposition
	y = keras.layers.Dense(10, activation = None)(y)
	y = keras.layers.Dense(50, activation = 'relu')(y)
	
	# without low-rank decomposition
	#y = keras.layers.Dense(50, activation = 'relu')(y)
	
	y = keras.layers.Dense(CLASS_NUM, activation = 'softmax')(y)
	return keras.models.Model(x, y)

def CNN_Model(input_shape, word_num, dim):
	x = keras.layers.Input(input_shape)
	y = keras.layers.Embedding(word_num + 1, dim, weights = [word_mat], input_length = PAD_LENGTH, trainable = False)(x)
	
	kernel_sizes = [2, 3, 4, 5]
	y_prime = None
	for kernel_size in kernel_sizes:
		y_conv = keras.layers.Conv1D(dim, kernel_size, activation = 'relu', padding = 'same')(y)
		y_conv = keras.layers.MaxPooling1D(PAD_LENGTH)(y_conv)
		y_conv = keras.layers.Dropout(0.5)(y_conv) # Dropout
		if y_prime is not None:
			y_prime = keras.layers.Concatenate()([y_prime, y_conv])
		else:
			y_prime = y_conv
	
	y = keras.layers.Flatten()(y_prime)
	y = keras.layers.Dense(CLASS_NUM, activation = 'softmax')(y)
	return keras.models.Model(x, y)

def RNN_Model(input_shape, word_num, dim):
	x = keras.layers.Input(input_shape)
	y = keras.layers.Embedding(word_num + 1, dim, weights = [word_mat], input_length = PAD_LENGTH, trainable = False)(x)
	
	# simple RNN
	y = keras.layers.SimpleRNN(50)(y)
	# GRU
	#y = keras.layers.GRU(50)(y)
	# LSTM
	#y = keras.layers.LSTM(50)(y)
	y = keras.layers.Dense(CLASS_NUM, activation = 'softmax')(y)
	return keras.models.Model(x, y)

fin = open(r'.\vec\sgns.sogounews.bigram-char', 'r', encoding = 'utf-8')
text = fin.readline()
word_num, dim = int(text.split()[0]), int(text.split()[1])
dict = {}
word_mat = np.zeros((word_num + 1, dim))
for i in range(word_num):
	text = fin.readline()
	text = text.split(' ')
	word_vec = []
	for j in range(1, dim + 1):
		word_vec.append(float(text[j]))
	word_mat[i + 1] = word_vec
fin.close()

input_shape = (PAD_LENGTH,)

x_train, y_train = get_data(r'.\data\train.text', r'.\data\train.label')
x_test, y_test = get_data(r'.\data\test.text', r'.\data\test.label')
y_train = keras.utils.to_categorical(y_train, CLASS_NUM)
y_test = keras.utils.to_categorical(y_test, CLASS_NUM)

model = RNN_Model(input_shape, word_num, dim)
model.compile(loss = keras.losses.categorical_crossentropy,
	optimizer = keras.optimizers.SGD(lr = 0.001, decay = 1e-5, momentum = 0.9, nesterov = True), metrics = ['acc'])
model.fit(x = x_train, y = y_train, batch_size = 100, epochs = 50, verbose = 2, validation_data = (x_test, y_test), callbacks = [callback(training_data = [x_train, y_train], validation_data = [x_test, y_test])])
