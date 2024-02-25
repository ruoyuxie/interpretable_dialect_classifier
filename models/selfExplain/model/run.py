import pytorch_lightning
from pytorch_lightning.callbacks import ModelCheckpoint, LearningRateMonitor
import random
import numpy as np
import pytorch_lightning as pl
import logging
from argparse import ArgumentParser
#import resource
from data import ClassificationData
from SE_XLNet import SEXLNet
import gc
import torch
import os

def get_train_steps(dm):
  total_devices = args.num_gpus * args.num_nodes
  train_batches = len(dm.train_dataloader()) // total_devices
  if args.accumulate_grad_batches is None:
    return (args.max_epochs * train_batches)
  else:
   return args.max_epochs * train_batches // args.accumulate_grad_batches




# rlimit = resource.getrlimit(resource.RLIMIT_NOFILE)
# resource.setrlimit(resource.RLIMIT_NOFILE, (4096, rlimit[1]))
# init: important to make sure every node initializes the same weights
SEED = 18
np.random.seed(SEED)
random.seed(SEED)
pl.utilities.seed.seed_everything(SEED)
pytorch_lightning.seed_everything(SEED)

if __name__ == "__main__":

  # argparser
  parser = ArgumentParser()
  parser.add_argument('--num_gpus', type=int)
  parser.add_argument('--batch_size', type=int, default=4)
  parser.add_argument('--clip_grad', type=float, default=1.0)
  parser.add_argument("--dataset_basedir", help="Base directory where the dataset is located.", type=str)
  parser.add_argument("--concept_store", help="Concept store file", type=str)
  parser.add_argument("--model_name", default='xlm-roberta-base', help="Model to use.")
  parser.add_argument("--gamma", default=0.01, type=float, help="Gamma parameter")
  parser.add_argument("--lamda", default=0.01, type=float, help="Lamda Parameter")
  parser.add_argument("--topk", default=100, type=int,help="Topk GIL concepts")
  parser.add_argument("--num_classes", type=int, help="Number of classes.")

  parser = pl.Trainer.add_argparse_args(parser)
  parser = SEXLNet.add_model_specific_args(parser)

  args = parser.parse_args()

  if torch.cuda.is_available():
      args.num_gpus = torch.cuda.device_count()
      args.accelerator = "cuda"
      args.devices = torch.cuda.device_count()
  else:
      args.num_gpus = len(str(args.gpus).split(","))

  # print(args)
  logging.info(f"Using {args.num_gpus} GPUs")
  logging.basicConfig(level=logging.INFO)

  # Step 1: Init Data
  logging.info("Loading the data module")
  dm = ClassificationData(basedir=args.dataset_basedir, tokenizer_name=args.model_name, batch_size=args.batch_size)
  training_steps = get_train_steps(dm)
  args.num_classes = dm.num_unique_labels

  # Step 2: Init Model
  logging.info("Initializing the model")
  model = SEXLNet(hparams=args)
  model.hparams.warmup_steps = int(training_steps * model.hparams.warmup_prop)
  lr_monitor = LearningRateMonitor(logging_interval='step')

  # Step 3: Start
  logging.info("Starting the training")
  if os.path.exists(args.dataset_basedir + '/checkpoints') == False:
      os.mkdir(args.dataset_basedir + '/checkpoints')

  # remove previous checkpoints
  for file in os.listdir(args.dataset_basedir + '/checkpoints'):
      os.remove(os.path.join(args.dataset_basedir + '/checkpoints', file))

  checkpoint_callback = ModelCheckpoint(
      dirpath=args.dataset_basedir + '/checkpoints',
      filename='{epoch}-{step}-{val_acc_epoch:.4f}',
      save_top_k=1,
      verbose=True,
      monitor='val_acc_epoch',
      mode='max'
  )
  torch.cuda.empty_cache()
  gc.collect()

  trainer = pl.Trainer.from_argparse_args(args, callbacks=[checkpoint_callback], val_check_interval=0.5, gradient_clip_val=args.clip_grad, track_grad_norm=2)
  trainer.fit(model, dm)
  # trainer.test()
