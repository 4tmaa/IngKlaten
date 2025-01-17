import argparse
import os.path

from .resolve import gen_output

def main():
    parser = argparse.ArgumentParser(description="");
    parser.add_argument('path', help="path to python file")
    parser.add_argument('-f', '--flag', help="Will output -m flag if path is importable",
                        action="store_true", default=True)
    parser.add_argument('-d', '--debug', help="Debug",
                        action="store_true")

    args = parser.parse_args()
    path = os.path.abspath(args.path)
    flag = args.flag
    debug = args.debug

    output = gen_output(path, flag, debug)
    print(output)
