import time

class EventTimer:
    def __init__(self, length, function, event_type, repeat=False):
        self._start = time.time()
        self._function = function
        self._length = length
        self.__type = event_type
        self._repeat = repeat
        self.__over = False

    def get_type(self):
        return self.__type

    def done(self):
        if time.time() - self._start > self._length:
            if self._repeat:
                self._start = time.time()
            else:
                return True
        self._function()
        return False
    
class IntervalEvent(EventTimer):
    def __init__(self, length, function, event_type, repeat=False):
        super().__init__(length, function, event_type, repeat)

    def done(self):
        if time.time() - self._start > self._length:
            self._function()
            if self._repeat:
                self._start = time.time()
            else:
                return True
        return False