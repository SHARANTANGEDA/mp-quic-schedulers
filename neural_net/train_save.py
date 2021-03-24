import logging
import os
import time

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.models import Sequential


def load_data(training_file):
	df = pd.read_csv(training_file)
	features = df[:, 1:]
	target = df[:, 0]
	target_map = {}
	for idx, value in enumerate(target.unique()):
		target_map[value] = idx

	return features, target, target_map


def train_save_model(training_file, epochs, output_dir):
	features, target, target_map = load_data(training_file)
	train_X, train_Y, test_X, test_Y = train_test_split(features, target, test_size=0.10)
	train_X, train_Y, val_X, val_Y = train_test_split(train_X, train_Y, test_size=0.1)
	model = Sequential()
	model.add(Dense(12, input_dim=8, activation='linear', name="input"))
	model.add(Dense(8, activation='relu'))
	model.add(Dense(1, activation='sigmoid', name="output"))

	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	logging.info("Model has been compiled")

	model.fit(train_X, train_Y, epochs=epochs, validation_data=(val_X, val_Y))

	# Save Model
	# Use TF to save the graph model instead of Keras save model to load it in Golang
	save_dir_path = os.path.join(output_dir, "model_"+str(int(time.time())))
	os.mkdir(save_dir_path)
	tf.saved_model.save(model, save_dir_path)
	# model.save_pretrained(save_dir_path, saved_model=True)
	logging.info("Model Saved at: {}".format(save_dir_path))

	# Evaluate
	test_loss, test_acc = model.evaluate(test_X, test_Y)
	logging.info("Test loss: {}, Test Accuracy: {}".format(test_loss, test_acc))
