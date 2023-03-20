import threading


def exception_handler(func):
    def _wrapper(*args, **kwargs):
        try:
            # do something before the function call
            result = func(*args, **kwargs)
            # do something after the function call
        except TypeError:
            print("TypeError")
        except IndexError:
            print("IndexError")
        # return result
    return _wrapper
