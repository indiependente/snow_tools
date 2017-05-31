#! /usr/local/bin/python

from sys import argv
from multiprocessing import Process, Manager
import time
import itertools 
import re

def do_work(in_queue, out_list):
	def any_word(patterns, data):
		return [p.search(data) for p in patterns]

	while True:
		item = in_queue.get()
		# print item
		line_no, line, patterns = item
		print line_no, line, patterns
		# exit signal 
		if line == [None]:
			return
		ans = any_word(patterns, line)
		print ans
		if not any(any_word(patterns, line)):
			return

		result = (line_no, line)

		out_list.append(result)


if __name__ == "__main__":
	NUM_WORKERS = 4
	filename = argv[1]
	words = argv[2:]
	print filename, words
	patterns = [re.compile(x) for x in words]
	
	manager = Manager()
	results = manager.list()
	work = manager.Queue(NUM_WORKERS)

	# start workers
	print 'start workers'
	pool = []
	for i in xrange(NUM_WORKERS):
		p = Process(target=do_work, args=(work, results))
		p.start()
		pool.append(p)

	# produce data
	print 'produce data'
	with open(filename) as f:
		iters = itertools.chain(f, (None,)*NUM_WORKERS)
		for lineno, line in enumerate(iters):
			work.put((lineno, line, patterns))

	print 'join'
	
	for p in pool:
		p.join()

	# get the results
	# example:  [(1, "foo"), (10, "bar"), (0, "start")]
	print results