import argparse

from alf.app import App


def main():
    parser = argparse.ArgumentParser(description='Start ALF')
    parser.add_argument('socket', metavar='S', type=str,
                        help='The path where the Unix socket will live')
    parser.add_argument('url', metavar='u', type=str,
                        help='The url where to send messages')
    args = parser.parse_args()

    alf = App(args.socket, args.url)
    alf.start()


if __name__ == '__main__':
    main()
