import frida
import sys
import pprint
from datetime import datetime

package_name = "com.playrix.township"
out_filename = "log/log_{}.txt".format(datetime.today().strftime("%Y%m%d_%H%M%S"))


def ts():
    return datetime.today().strftime("%d %H:%M:%S")


def file_and_stdout(arrOutput=[], padding=False):

    if isinstance(arrOutput, str):
        arrOutput = [arrOutput]

    prefix = ' '*46 if padding else ''

    with open(out_filename, 'at') as fout:
        for s in arrOutput:
            fout.write(prefix + s + '\n')
            print(prefix + s)


def log(thid=None, level=None, func_name=None, msg=None, data=None):
    s = "{0} | T:{1:5s} | {2:1s} | {3:15s} | {4}".format(ts(), thid, level, func_name, msg)
    file_and_stdout([s], False)

    if data:
        s = "{}".format(data)
        file_and_stdout([s], True)


def message_trace(thid, level, func_name, msg, data):
    log(thid=thid, level=level, func_name=func_name, msg=msg)
    length_list = [6, 7, 4]
    
    for d in data:
        addr = d.get('address', '')
        name = d.get('name', '')
        module = d.get('moduleName', '')
        length_list[0] = max( length_list[0], len(addr or '') )
        length_list[1] = max( length_list[1], len(name or '') )
        length_list[2] = max( length_list[2], len(module or '') )

    s = []
    fmt = ''
    fmt += '{0:' + str(length_list[2]) + 's} '
    fmt += '{1:' + str(length_list[0]) + 's} '
    fmt += '{2:' + str(length_list[1]) + 's} '
    s.append(fmt.format('Module', 'Address', 'Name'))

    s.append("-" * (sum(length_list) + 3))

    for d in data:
        addr = d.get('address', '')
        name = d.get('name', '')
        module = d.get('moduleName', '')
        # filename = d.get('fileName', '')
        # lineNo = d.get('lineNumber', '')

        s.append(fmt.format(module or '', addr or '', name or ''))
    file_and_stdout(s, True)


def message_send(payload):
    level = '{0:1s}'.format(payload.get('log_level', ''))
    func_name = '{0:15s}'.format(payload.get('function', '')[:15])
    msg = payload.get('msg', '')
    data = payload.get('data', '')
    thid = '{0:5d}'.format(payload.get('thread_id', 0))

    if level == 'T' :
        message_trace(thid=thid, level=level, func_name=func_name, msg=msg, data=data)
    
    elif level == 'P':
        log(thid=thid, level=level, func_name=func_name, msg=msg)
        _dump_list = list(data.split('\n'))
        file_and_stdout(_dump_list, True)
    
    else:    
        log(thid=thid, level=level, func_name=func_name, msg=msg, data=data)


def get_messages_from_js(message, data):
    _type = message.get('type', None)
    _payload = message.get('payload', None)
    
    if _type == 'send':
        message_send(_payload)
    
    else:
        log(thid='?', level='?', func_name='?', msg='unknown', data=message )


def js():
    with open('js/township.js', 'rb') as fin:
        data = fin.read().decode('UTF-8')
        return data

device = frida.get_usb_device()
pid = device.spawn([package_name])

proc = device.attach(pid)

script = proc.create_script(js())
script.on('message', get_messages_from_js)
script.load()

device.resume(pid)

sys.stdin.read()
