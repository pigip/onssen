import sys
sys.path.append('../../../../../onssen/')

from onssen import data, loss, nn, utils
from attrdict import AttrDict
import argparse
import torch
import json


def main():
    parser = argparse.ArgumentParser(description='Parse the config path')
    parser.add_argument("-c", "--config", dest="path",
                        help='The path to the config file. e.g. python run.py --config config.json')

    config = parser.parse_args()
    with open(config.path) as f:
        args = json.load(f)
        args = AttrDict(args)
    device = torch.device(args.device)
    args.model = nn.chimera(**(args['model_options']))
    args.model.to(device)
    args.train_loader = data.wsj0_2mix_dataloader(args.model_name, args.feature_options, 'tr', device)
    args.valid_loader = data.wsj0_2mix_dataloader(args.model_name, args.feature_options, 'cv', device)
    args.optimizer = utils.build_optimizer(args.model.parameters(), args.optimizer_options)
    args.loss_fn = loss.loss_chimera_psa
    trainer = utils.trainer(args)
    trainer.run()
    
    tester = utils.tester(args)
    tester.eval()





if __name__ == "__main__":
    main()
