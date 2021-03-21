import argparse
import logging
import os
from datetime import datetime

import pandas as pd
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
	model.add(Dense(12, input_dim=8, activation='linear'))
	model.add(Dense(8, activation='relu'))
	model.add(Dense(1, activation='sigmoid'))

	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

	model.fit(train_X, train_Y, epochs=epochs, validation_data=(val_X, val_Y))

	# Save Model
	save_dir_path = os.path.join(output_dir, str(datetime.utcnow()))
	os.mkdir(save_dir_path)
	model.save_pretrained(save_dir_path, saved_model=True)
	logging.info("Model Saved at: {}".format(save_dir_path))

	# Evaluate
	test_loss, test_acc = model.evaluate(test_X, test_Y)
	logging.info("Test loss: {}, Test Accuracy: {}".format(test_loss, test_acc))
	return 1


parser = argparse.ArgumentParser(description='Train & Save Model')
parser.add_argument('--epochs', type=int, dest="epochs", help="Num of epochs to run", default=3)
parser.add_argument('--training_file', type=str, dest="training_file", help="Absolute Path to training file", required=True)
parser.add_argument('--output_dir', type=str, dest="output_dir", help="Absolute Path to output dir", required=True)

args = parser.parse_args()

logs_dir = os.path.join(os.getenv("PROJECT_HOME_DIR"), "nn_logs")
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(logs_dir, f'{datetime.now()}.txt'), filemode='w+',
										format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
										datefmt='%H:%M:%S', level=logging.DEBUG)
logging.getLogger().setLevel(logging.INFO)
train_save_model(args.training_file, args.epochs, args.output_dir)
