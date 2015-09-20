from memspector import Memspector, MAIN_THREAD_NAME
import unittest
from datetime import datetime


messages = []


class TestMemspector(unittest.TestCase):

    def test_spectate(self):
        ms = Memspector()
        ms.spectate('1+1')
        self.assertEqual(len(ms.memdata._diffs[MAIN_THREAD_NAME]), 1)

    def test_fn_call(self):
        ms = Memspector()
        ms.spectate('''
def a(): return
a()
''')
        self.assertEqual(len(ms.memdata._diffs[MAIN_THREAD_NAME]), 2)

    def test_threading(self):
        ms = Memspector()
        ms.spectate('''
import threading
def a(): return
def b(): return
def launcher(fn, times):
    for _ in xrange(times):
        fn()
t1 = threading.Thread(target=launcher, args=(a, 1))
t2 = threading.Thread(target=launcher, args=(b, 1))
t1.start()
t2.start()
t1.join()
t2.join()
''')
        self.assertEqual(len(ms.memdata._diffs), 3)

    def test_exclude_all(self):
        ms = Memspector(exclude_patterns=['.*'])
        ms.spectate('1+1')
        self.assertEqual(len(ms.memdata._diffs), 0)

    def test_multiple_calls(self):
        ms = Memspector(enable_gc=True)
        time_before = datetime.now()
        ms.spectate('''
def a(): return
for _ in xrange(1000):
    a()
''')
        time_after = datetime.now()
        messages.append('Execution time of 1000 function calls with gc: {0}'
                        .format(time_after - time_before))
        self.assertEqual(len(ms.memdata._diffs[MAIN_THREAD_NAME]['<string>:a()']), 1000)

    def test_multiple_calls_with_gc(self):
        ms = Memspector()
        time_before = datetime.now()
        ms.spectate('''
def a(): return
for _ in xrange(1000):
    a()
''')
        time_after = datetime.now()
        messages.append('Execution time of 1000 function calls: {0}'
                        .format(time_after - time_before))
        self.assertEqual(len(ms.memdata._diffs[MAIN_THREAD_NAME]['<string>:a()']), 1000)

    def test_multiple_skipped_calls(self):
        ms = Memspector(exclude_patterns=['.*'])
        time_before = datetime.now()
        ms.spectate('''
def a(): return
for _ in xrange(100000):
    a()
''')
        time_after = datetime.now()
        messages.append('Execution time of 100000 skipped function calls: {0}'
                        .format(time_after - time_before))
        self.assertEqual(len(ms.memdata._diffs), 0)


if __name__ == '__main__':
    unittest.main(exit=False)
    print '\n'.join(messages)
