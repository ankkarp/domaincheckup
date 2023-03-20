import logging


from socket import gaierror


def socket_exc(func):
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except gaierror:
            logging.warning(f'Не удалось подключиться к {args[-1]}')
        except Exception as e:
            logging.error(f'{args[-1]}: {e}')
    return _wrapper
