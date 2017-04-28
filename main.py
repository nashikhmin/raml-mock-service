import argparse

from server.mock import Mock


def start_program():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', dest='file', help='Raml specification file')
    parser.add_argument('-p', '--port', dest='port', default=5000, help='server port')
    parser.add_argument('-d', '--debug', action="store_true", help='enable debug mode')
    args = parser.parse_args()

    file = args.file
    mock = Mock(file)
    mock.start(args.port, debug=args.debug)


if __name__ == '__main__':
    start_program()