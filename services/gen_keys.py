# Generator function to create unique keys
def key_generator(prefix):
    counter = 0
    while True:
        yield f"{prefix}_{counter}"
        counter += 1
