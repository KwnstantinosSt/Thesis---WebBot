import argparse


def myArgs():
    try:
        parser = argparse.ArgumentParser(description='Enhanced Web Bot')
        parser.add_argument('--method', dest='method', type=str,
                            help='[REQUIRED] Please enter the name of the method ["bfs" or "dfs"] you want to use.', required=True)
        parser.add_argument('--depth', dest='depth', type=int,
                            help='[REQUIRED] Please enter a depth number you want to reach the algorithm from the parent url.', required=True)
        parser.add_argument('--urls', dest='urls', type=str,
                            help='[REQUIRED] Please enter the full url of each site (for multiple urls use comma "," between urls).', required=True, action='append')
        parser.add_argument('--multithread', dest='multithread', type=str,
                            help='[OPTIONAL] Please enter [yes or no] to multithread the program.', required=False)
        parser.add_argument('--continue', dest='continue', type=int,
                            help='[OPTIONAL] Please enter proper bot run id to continue the program.', required=False)
        parser.add_argument('--version', action='version',
                            version='Web Bot -- Version: 1.0')
        args = parser.parse_args()
        return args
    except Exception as e:
        print(e)
