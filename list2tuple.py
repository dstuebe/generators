def coroutine(func):
  """ A helper function decorator from Beazley"""
  def start(*args, **kwargs):
    g = func(*args, **kwargs)
    g.next()
    return g
  return start

@coroutine
def cotuple2list():
  """This does the work"""
  result = None
  while True:
    (tup, co_pool) = (yield result)
    result = list(tup)
    # I don't like using append. So I am changing the data in place.
    for (i,x) in enumerate(result):
      # consider using "if hasattr(x,'__iter__')"
      if isinstance(x,tuple):
        result[i] = co_pool[0].send((x, co_pool[1:]))


@coroutine
def colist2tuple():
  """This does the work"""
  result = None
  while True:
    (lst, co_pool) = (yield result)
    # I don't like using append so I am changing the data in place...
    for (i,x) in enumerate(lst):
      # consider using "if hasattr(x,'__iter__')"
      if isinstance(x,list):
        lst[i] = co_pool[0].send((x, co_pool[1:]))
    result = tuple(lst)

def list2tuple(a):
  return tuple((list2tuple(x) if isinstance(x, list) else x for x in a))

def tuple2list(a):
  return list((tuple2list(x) if isinstance(x, tuple) else x for x in a))


def make_test(m, n):
  # Test data function taken from HYRY's post!
  return [[range(m), make_test(m, n-1)] for i in range(n)]

if __name__ == "__main__":
  import timeit
  #t = make_test(20, 8)
  number = 10
  repeat = 5
  depth = 8
  breadth = 25
  print "Time:  %s" % [v/ number for v in timeit.repeat('list2tuple(t)', setup='from __main__ import list2tuple, make_test, depth, breadth; t = make_test(breadth, depth)', number=number, repeat=repeat)]
  #timeit colist2tuple_pool[0].send((t, colist2tuple_pool[1:]))

  colist2tuple_pool = [colist2tuple() for i in xrange(breadth+1) ]
  print "Time:  %s" % [v/ number for v in timeit.repeat('colist2tuple_pool[0].send((t, colist2tuple_pool[1:]))', setup='from __main__ import colist2tuple_pool, make_test, depth, breadth; t = make_test(breadth, depth)', number=number, repeat=repeat)]


