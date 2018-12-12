import tensorflow as tf

from models.cae_model import CAEModel
from trainers.cae_trainer import CAETrainer
from data_loader.cae_data import CAEData
from utils.config import process_config
from utils.dirs import create_dirs
from utils.logger import Logger
from utils.utils import get_args

def main():
    try:
        args = get_args()
        config = process_config(args.config)

    except:
        print("Missing or invalid arguments")
        exit(0)

    create_dirs([config.summary_dir,config.checkpoint_dir])
    sess = tf.Session()
    data = CAEData(config)
    model = CAEModel(config)
    logger = Logger(sess,config)
    trainer = CAETrainer(sess,model,data,config,logger)
    sess.run(tf.global_variables_initializer())
    model.load(sess)
    trainer.train()

if __name__ == '__main__':
    main()
