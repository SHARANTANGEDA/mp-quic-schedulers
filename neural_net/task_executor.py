import argparse
import logging
import os
import time
from datetime import datetime

from neural_net.train_save import train_save_model

project_home_dir = os.getenv("PROJECT_HOME_DIR")

parser = argparse.ArgumentParser(description='Train & Save Model')
parser.add_argument('--epochs', type=int, dest="epochs", help="Num of epochs to run", default=3)
parser.add_argument('--training_file', type=str, dest="training_file", help="Absolute Path to training file", required=True)
parser.add_argument('--output_dir', type=str, dest="output_dir", help="Absolute Path to output dir", required=True)
args = parser.parse_args()

logs_dir = os.path.join(project_home_dir, "nn_logs")
os.makedirs(logs_dir, exist_ok=True)


logging.basicConfig(filename=os.path.join(logs_dir, f'{datetime.now()}.txt'), filemode='w+',
										format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
logging.getLogger().setLevel(logging.INFO)

while True:
	time.sleep(5*60)
	if not os.path.isdir(os.path.join(project_home_dir, "model_output")) or os.path.isfile(os.path.join(
		project_home_dir, "online_training", "train.txt")):
		logging.warning("Skipping training for another 5 mins, as required data is not available yet!")
		continue
	logging.info("Starting to Train & save the model")
	train_save_model(args.training_file, args.epochs, args.output_dir)
