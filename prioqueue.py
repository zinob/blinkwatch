#!/usr/bin/python3
import unittest
from collections import namedtuple


class prio_queue:
	"""Dumbest possible prioQueue implementation"""
	def __init__(self,key_index,dedup_key=None):
		self._index=key_index
		self._queue=[]
		self._dup_ix=dedup_key

	def push(self,item):
		target=None
		keyval=item[self._index]
		dup_ix=self._dup_ix
		dup=None

		for n,i in enumerate(self._queue):
			if target == None and keyval < i[self._index]:
				target=n
			if None != dup_ix and item[dup_ix] == i[dup_ix]:
				dup=n

		if not None in [dup,target] and dup >= target:
			return
				
		if target != None:
			self._queue.insert(target,item)
		else:
			self._queue.append(item)

		if dup != None and (target == None or dup < target):
			del	self._queue[dup]
		return


	def is_empty(self):
		return self._queue == []

	def peek(self):
		return self._queue[0]

	def pop(self):
		return self._queue.pop(0)

class ParametrizedTestCase(unittest.TestCase):
	""" TestCase classes that want to be parametrized should
		inherit from this class.
	"""
	def __init__(self, methodName='runTest', param=None):
		super(ParametrizedTestCase, self).__init__(methodName)
		self.param = param
	
	@staticmethod
	def parametrize(testcase_klass, param=None):
		""" Create a suite containing all tests taken from the given
			subclass, passing them the parameter 'param'.
		"""
		testloader = unittest.TestLoader()
		testnames = testloader.getTestCaseNames(testcase_klass)
		suite = unittest.TestSuite()
		for name in testnames:
			suite.addTest(testcase_klass(name, param=param))
		return suite

event=namedtuple("test",["order","id"])
class CommonTests(ParametrizedTestCase):
	def setUp(s):
		s.e0=event(1,2)
		s.e1=event(2,2)
		s.e2=event(3,2)
		s.q=prio_queue(0, s.param['dedup_key'])

	def test_init(s):
		s.assertIsInstance(s.q,prio_queue)

	def test_is_empty(s):
		s.assertEqual(s.q.is_empty(),True)
		s.q.push(s.e1)
		s.assertEqual(s.q.is_empty(),False)
		s.q.pop()
		s.assertEqual(s.q.is_empty(),True)

	def test_peek(s):
		s.assertRaises(IndexError,s.q.peek)
		s.q.push(s.e1)
		s.assertEqual(s.q.peek(),s.e1)
		s.q.push(s.e0)
		s.assertEqual(s.q.peek(),s.e0)
		s.q.push(s.e2)
		s.assertEqual(s.q.peek(),s.e0)
		n=0
		while not s.q.is_empty():
			s.assertIsInstance(s.q.pop(),event)
			n+=1
			s.assertLess(n,10)
		s.assertRaises(IndexError,s.q.peek)

	def test_ordered_insert(s):
		s.q.push(s.e1)
		s.assertEqual(s.q.pop(),s.e1)
		s.q.push(s.e0)
		s.q.push(s.e1)
		s.q.push(s.e2)
		s.assertEqual(s.q.pop(),s.e0)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertEqual(s.q.pop(),s.e2)

	def test_out_of_order(s):
		s.q.push(s.e2)
		s.assertEqual(s.q.peek(),s.e2)
		s.q.push(s.e1)
		s.assertEqual(s.q.peek(),s.e1)
		s.q.push(s.e0)
		s.assertEqual(s.q.pop(),s.e0)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertEqual(s.q.pop(),s.e2)
		
class TestNoDedup(unittest.TestCase):
	def setUp(s):
		s.e0=event(1,2)
		s.e1=event(2,2)
		s.e2=event(3,2)
		s.q=prio_queue(0)

	def test_ordered_insert(s):
		s.q.push(s.e1)
		s.q.push(s.e1)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertEqual(s.q.pop(),s.e1)
		s.q.push(s.e1)
		s.q.push(s.e1)
		s.q.push(s.e2)
		s.q.push(s.e2)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertEqual(s.q.pop(),s.e2)
		s.assertEqual(s.q.pop(),s.e2)

	def test_out_of_order(s):
		s.q.push(s.e2)
		s.q.push(s.e1)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertEqual(s.q.pop(),s.e2)
		s.q.push(s.e0)
		s.assertEqual(s.q.peek(),s.e0)
		s.q.push(s.e1)
		s.q.push(s.e2)
		s.assertEqual(s.q.peek(),s.e0)
		s.q.push(s.e0)
		s.q.push(s.e1)
		s.assertEqual(s.q.pop(),s.e0)
		s.assertEqual(s.q.pop(),s.e0)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertEqual(s.q.pop(),s.e1)

class TestDedup(unittest.TestCase):
	def setUp(s):
		s.e0=event(1,1)
		s.e1=event(2,1)
		s.e2=event(3,1)
		s.e0b=event(1,2)
		s.e1b=event(2,3)
		s.e2b=event(3,4)
		s.q=prio_queue(0,1)

	def test_simple_dup(s):
		s.q.push(s.e1)
		s.q.push(s.e1)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertRaises(IndexError,s.q.pop)
		s.q.push(s.e0)
		s.q.push(s.e1)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertRaises(IndexError,s.q.pop)

	def test_reversed_dup(s):
		s.q.push(s.e1)
		s.q.push(s.e0)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertRaises(IndexError,s.q.pop)

	def test_reversed_dup(s):
		s.q.push(s.e0)
		s.q.push(s.e1)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertRaises(IndexError,s.q.pop)

	def test_mixin(s):
		s.q.push(s.e0)
		s.q.push(s.e0b)
		s.q.push(s.e1)
		s.q.push(s.e1b)
		s.q.push(s.e2b)
		s.q.push(s.e0)

		s.assertEqual(s.q.pop(),s.e0b)
		s.assertEqual(s.q.pop(),s.e1)
		s.assertEqual(s.q.pop(),s.e1b)
		s.assertEqual(s.q.pop(),s.e2b)
		s.assertRaises(IndexError,s.q.pop)

if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest(ParametrizedTestCase.parametrize(CommonTests, param={"dedup_key":None}))
	suite.addTest(ParametrizedTestCase.parametrize(CommonTests, param={"dedup_key":0}))
	suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestNoDedup))
	suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestDedup))
	unittest.TextTestRunner(verbosity=2).run(suite)


