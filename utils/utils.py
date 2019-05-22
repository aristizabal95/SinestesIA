import argparse


def get_args():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        '-c', '--config',
        metavar='C',
        default='None',
        help='The Configuration file')
    argparser.add_argument(
        '--caeconfig',
        metavar='CAE',
        default='configs/cae_config.json',
        help='The configuration file for CAE model'
    )
    argparser.add_argument(
        '--rnnconfig',
        metavar='RNN',
        default='configs/rnn_config.json',
        help='The configuration file for RNN model'
    )
    argparser.add_argument(
        '--actionsconfig',
        metavar='Actions',
        default='configs/actions_config.json',
        help='The configuration file for the Actions Model'
    )
    argparser.add_argument(
        '-l', '--length',
        metavar='L',
        default='150',
        help='The length of each dream sequence'
    )
    argparser.add_argument(
        '-r', '--random',
        metavar='R',
        default='1',
        help='Whether to add randomness to dream sequence'
    )
    args = argparser.parse_args()
    return args
