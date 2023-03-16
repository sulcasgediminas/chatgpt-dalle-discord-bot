def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Logging call to {func.__name__} with args: {args} and kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@logger
def my_func(x, y):
    return x + y


print(my_func(10, 10))