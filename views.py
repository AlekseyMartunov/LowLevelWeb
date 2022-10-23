def index():
    with open('templates/index.html') as file:
        return file.read()


def blog():
    with open('templates/blog.html') as file:
        return file.read()