from threading import Lock


class ConcurrentFloat(float):
    def __init__(self, initial_value: float = 0.0):
        self.value = initial_value
        self.lock = Lock()

    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self):
        self.lock.release()
