from functools import wraps


def prettify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'Function Name: {func.__name__}')
        if args:
            print('\nPositional Arugments:')
            for i, arg in enumerate(args, 1):
                print(f'    arg {i} = {arg}')
        if kwargs:
            print('\nKeyword Arguments:')
            for k,v in kwargs.items():
                print(f'    {k} = {v}')
                
        print('\nReturn Value: ')
        return func(*args, **kwargs)
    return wrapper



@prettify
def example_func(*args, bitch=None, **kwargs):
    return '    this function does nothing'


print(example_func(1,'fifty-five', hi='mom'))


