import socket
from views import index, blog

URLS = {
    '/': index,
    '/blog': blog
}


def parse(request):
    parsed = request.split()
    method = parsed[0]
    url = parsed[1]
    return method, url


def generate_headers(method, url):
    if not method == 'GET':
        return 'HTTP/1.1 405 method not allowed\n\n', 405

    if url not in URLS:
        return 'HTTP/1.1 404 not found\n\n', 404

    return 'HTTP/1.1 200 OK', 200


def generate_body(code, url):
    if code == 404:
        return '<h1>404</h1><p>NOT FOUND!</p>'

    if code == 405:
        return '<h1>405</h1><p>method not allowed</p>'

    return URLS[url]()


def generate_response(request):
    method, url = parse(request)
    headers, code = generate_headers(method, url)
    body = generate_body(code, url)

    return (headers + '\n\n' + body).encode()


def main():
    print('start...')
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.bind(('localhost', 5000))
    my_socket.listen()

    while True:
        client_socked, addr = my_socket.accept()
        request = client_socked.recv(1024)

        if request:
            response = generate_response(request.decode('utf-8'))
            client_socked.sendall(response)
        client_socked.close()


if __name__ == '__main__':
    main()
