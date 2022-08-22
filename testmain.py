import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    args = parser.parse_args(argv)
    print(f'Hello {args.name}')


if __name__ == '__main__':
    sys.exit(main())
