import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str)
    parser.add_argument('way', type=str)
    args = parser.parse_args()
    for root, dirs, files in os.walk(args.way):
        for file in files:
            if file == args.name:
                path_file = os.path.join(root, file)
                print(path_file, 'True')
