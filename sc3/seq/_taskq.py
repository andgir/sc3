
import heapq
import itertools


__all__ = ['TaskQueue']


class TaskQueue():
    """
    This class is an encapsulation of the algorithm found in heapq
    documentation. heapq module in itself use the same principles as
    SuperCollider's clocks implementation. TaskQueue is not thread safe.
    """

    _REMOVED = '<removed-task>'

    def __init__(self):
        self._init()

    def _init(self):
        self._queue = []
        self._entry_finder = {}
        self._counter = itertools.count()
        self._removed_counter = 0

    def add(self, time, task):
        'Add a new task or update the time of an existing task.'
        if task in self._entry_finder:
            self.remove(task)
        count = next(self._counter)
        entry = [time, count, task]
        self._entry_finder[task] = entry
        heapq.heappush(self._queue, entry)

    def remove(self, task):
        'Remove an existing task. Raise KeyError if not found.'
        entry = self._entry_finder.pop(task)
        entry[-1] = type(self)._REMOVED
        self._removed_counter += 1

    def pop(self):
        '''Remove and return the lowest time entry as a tuple (time, task).
        Raise KeyError if empty.'''
        while self._queue:
            time, count, task = heapq.heappop(self._queue)
            if task is not type(self)._REMOVED:
                del self._entry_finder[task]
                return (time, task)
            else:
                self._removed_counter -= 1
        raise KeyError('pop from an empty task queue')

    def peek(self):
        '''Return the lowest time entry as a tuple (time, task) without
        removing it.'''
        for i in range(len(self._queue)):  # Can have <removed-task>s first.
            time, count, task = self._queue[i]
            if task is not type(self)._REMOVED:
                return (time, task)
        raise KeyError('peek from an empty task queue')

    def empty(self):
        'Return True if queue is empty.'
        return (len(self._queue) - self._removed_counter) == 0

    def clear(self):
        'Reset the queue to initial state (remove all tasks).'
        self._init()

    # NOTE: implementar __iter__ y copy()
