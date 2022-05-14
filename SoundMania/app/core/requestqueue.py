from dataclasses import dataclass
from typing import Callable

import logging
logger = logging.getLogger("RequestQueue")


@dataclass
class _RequestItem:
    callback: Callable
    timeout: int
    preprocess_callback: Callable[[], None] = lambda: None
    postprocess_callback: Callable[[], None] = lambda: None


class RequestQueue:
    def __init__(self, maxsize: int = 100):
        self.maxsize = maxsize
        self.blocked = False
        
        self._req_queue: list[_RequestItem] = []
        self._in_process: _RequestItem | None = None
        self._timeout = 0


    def add(self, request: Callable, timeout: int = 0) -> None:
        """ Create and push a new request to the queue from a callable. """
        if timeout < 0:
            raise ValueError("Request timeout duration cannot be negative.")
        
        self._push_request(_RequestItem(request, timeout))
        
    
    def add_blocking(self, request: Callable, timeout: int) -> None:
        """ Create and push a new blocking request to the queue from a callable. 
        
            For the duration of the request being processed, RequestQueue will block any incoming requests. 
        """
        if timeout <= 0:
            raise ValueError("Blocked request timeout duration must be greater than 0.")
        
        preprocessor = lambda: setattr(self, "blocked", True)
        postprocessor = lambda: setattr(self, "blocked", False)
        
        self._push_request(_RequestItem(request, timeout, preprocessor, postprocessor))
        
        
    def process(self, dt: int) -> None:
        """ Process the next request in queue. 
        
            Args:
                dt: elapsed time since the last frame 
        """
        if self._timeout > 0:
            self._timeout -= dt
        else:
            if self._in_process:
                self._in_process.postprocess_callback()
                self._in_process = None
                
            if self._req_queue:
                request = self._req_queue.pop(0)
                request.preprocess_callback()
                request.callback()
                
                self._timeout = request.timeout
                self._in_process = request
            
            
    def _push_request(self, request: _RequestItem) -> None:
        if len(self._req_queue) >= self.maxsize:
            logger.critical("Queue is full. An incoming request has been ignored")
            return
        
        if self.blocked:
            logger.debug("An incoming request has been blocked")
            return
        
        self._req_queue.append(request)
        