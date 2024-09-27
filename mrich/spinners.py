from .console import console


# spinners
def spinner(*args, **kwargs):
    return console.status(*args, spinner="line", **kwargs)


def loading(*args, **kwargs):
    return console.status(*args, spinner="aesthetic", **kwargs)


def clock(*args, **kwargs):
    return console.status(*args, spinner="clock", **kwargs)
