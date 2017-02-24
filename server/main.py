from server.mock import Mock


if __name__ == '__main__':
    file = "example.raml"
    mock = Mock(file)
    mock.start()