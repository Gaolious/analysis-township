import hashlib
import inspect
import json
import logging


class Logger(object):
    def __init__(self, name='default'):
        self.logger = logging.getLogger(name)

    def _gen(self, name: str, func: str, **kwargs):
        msg = json.dumps(
            {
                'name': name,
                'func': func,
                'data': kwargs
            }
        )
        return msg

    def error(self, name: str, func: str, **kwargs):
        self.logger.error(msg=self._gen(name=name, func=func, **kwargs))

    def exception(self, name: str, func: str, **kwargs):
        self.logger.exception(msg=self._gen(name=name, func=func, **kwargs))

    def info(self, name: str, func: str, **kwargs):
        self.logger.info(msg=self._gen(name=name, func=func, **kwargs))

    def debug(self, name: str, func: str, **kwargs):
        self.logger.debug(msg=self._gen(name=name, func=func, **kwargs))

    def warning(self, name: str, func: str, **kwargs):
        self.logger.warning(msg=self._gen(name=name, func=func, **kwargs))


def hash10(msg):

    MAX_INT = 9223372036854775808  # 2^63
    if not msg or not isinstance(msg, str):
        msg = ''
    try:
        msg = bytes(msg, 'utf-8')
        m = hashlib.md5(msg)
        # max 2**64 and modular with 2**63
        return int(m.hexdigest()[:16], 16) % MAX_INT
    except:
        pass
    return 0