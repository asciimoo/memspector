import gc
import re
import logging

from collections import defaultdict
from sys import setprofile, getsizeof
from threading import current_thread, setprofile as threading_setprofile
from traceback import print_exc


MAIN_THREAD_NAME = 'main_thread'


def get_memory_usage():
    return sum(map(getsizeof, gc.get_objects()))


def get_function_id(frame):
    code = frame.f_code
    function_name = code.co_name
    filename = code.co_filename
    if function_name == '<module>':
        return filename
    return '{0}:{1}()'.format(filename,
                              function_name)


def spawn_defaultdict(inner_type):
    def init_defaultdict():
        return defaultdict(inner_type)
    return init_defaultdict


class Memdata(object):
    """docstring for Memdata"""
    def __init__(self):
        super(Memdata, self).__init__()
        self._incomplete_calls = defaultdict(spawn_defaultdict(list))
        self._diffs = defaultdict(spawn_defaultdict(list))

    def add(self, thread_id, function_id, call_type):
        if call_type == 'call':
            self._incomplete_calls[thread_id][function_id].append(get_memory_usage())
        elif call_type == 'return':
            try:  # TODO handle exceptions/exception returns
                call_memory_usage = self._incomplete_calls[thread_id][function_id].pop()
            except:
                return
            self._diffs[thread_id][function_id].append((call_memory_usage,
                                                        get_memory_usage() - call_memory_usage))


class Memspector(object):
    """docstring for Memspector"""
    def __init__(self, enable_gc=False, exclude_patterns=None):
        super(Memspector, self).__init__()
        self.memdata = Memdata()
        self.exclude_regex = None
        self.enable_gc = enable_gc
        if exclude_patterns:
            self.exclude_regex = re.compile('({0})'.format(')|('.join(exclude_patterns)), re.U)

    def main_callback(self, frame, call_type, frame_args, thread_id=MAIN_THREAD_NAME):
        if call_type.startswith('c_'):
            return
        function_id = get_function_id(frame)
        if self.exclude_regex:
            if self.exclude_regex.search(function_id):
                return
        logging.debug("tracing %s", function_id)
        if self.enable_gc:
            gc.collect()
        self.memdata.add(thread_id, function_id, call_type)

    def thread_callback(self, *args):
        return self.main_callback(*args, thread_id=current_thread().name)

    def spectate(self, expr, globals=None, locals=None):
        if globals is None:
            import __main__
            globals = __main__.__dict__
        if locals is None:
            locals = globals
        threading_setprofile(self.thread_callback)
        setprofile(self.main_callback)
        exception_occured = False
        try:
            if expr.endswith('.py'):
                execfile(expr, globals, locals)
            else:
                exec(expr, globals, locals)
        except Exception:
            exception_occured = True
        except:
            print '[!] command interrupted'
        finally:
            setprofile(None)
            threading_setprofile(None)
        if exception_occured:
            print '[!] Exception occured'
            print_exc()

    def dump_diffs(self):
        for thread_name, thread_data in self.memdata._diffs.iteritems():
            for fn_name, fn_data in thread_data.iteritems():
                print '{0:<60} thread: {1}'.format(fn_name, thread_name)
                print '{0:^15}{1:^15}'.format('total memory', 'diff')
                print '\n'.join('{0:15,}{1:15,}'.format(*x) for x in fn_data)
                print


def argparser():
    import argparse
    argp = argparse.ArgumentParser(description='memspector - inspect memory usage of python functions')
    argp.add_argument('-x', '--exclude',
                      help='Regex to filter out unwanted functions',
                      action='append',
                      type=unicode,
                      metavar='REGEX',
                      default=None)
    argp.add_argument('-g', '--enable-gc',
                      action='store_true',
                      help='Collect garbage after each call - slower, but sometimes more accurate',
                      default=False)
    argp.add_argument('-v', '--verbose',
                      action='store_true',
                      help='Verbose mode',
                      default=False)
    argp.add_argument('file',
                      metavar='FILE',
                      help='Target python file')
    return vars(argp.parse_args())


def __main():
    args = argparser()

    if args['verbose']:
        logging.basicConfig(level=logging.DEBUG)

    spector = Memspector(args['enable_gc'], args['exclude'])
    spector.spectate(args['file'])
    spector.dump_diffs()


if __name__ == '__main__':
    __main()
