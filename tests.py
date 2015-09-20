from memspector import Memspector, MAIN_THREAD_NAME
import unittest


class TestMemspect(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
