from typing import Callable

import logging
logger = logging.getLogger("RequestQueue")




class _Request:
    def __init__(self, callback: Callable, timeout: int):
        self.callback = callback
        self.timeout = timeout


class RequestQueue:
    def __init__(self, maxsize: int = 5):
        self.maxsize = maxsize
        self._req_queue: list[_Request] = []
        self._timeout = 0


    def add(self, request: Callable, timeout: int = 0) -> None:
        """ Create and add a new request to the queue from a callable. """
        if len(self._req_queue) >= self.maxsize:
            logger.critical("Queue is full. An incoming request has been ignored")
            return
        
        self._req_queue.append(_Request(request, timeout))
        
        
    def process(self, dt: int) -> None:
        """ Process the next request in queue. 
        
            Args:
                dt: elapsed time since the last frame 
        """
        if self._timeout > 0:
            self._timeout -= dt
        else:
            if not self._req_queue:
                return
            
            request = self._req_queue.pop(0)
            request.callback()
            
            self._timeout = request.timeout
        