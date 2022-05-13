from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Callable


class callback_property(property):
    """ Descriptor class for callable properties. 

        callback_property makes sure a property is always callable, giving it 
        a NO_OP method callback by default. 

        A callbackproperty instance can be set to either a callable method or
        `None`, which works the same way as deleting the propetry with the `del`
        keyword and resets the callback to NO_OP.

        When setting a callbackproperty to a callable, it's automatically injected
        with a `self`-like argument.
    """
    def __init__(self):
        """ Make a new descriptor property for callable types. """
        super().__init__(self.getter, self.setter, self.deleter)


    @staticmethod
    def NO_OP(*args, **kwargs) -> None:
        pass
    
    
    def __set_name__(self, obj: type, name: str) -> None:
        self.callback_accessor = f"_{name}"
        setattr(obj, self.callback_accessor, self.NO_OP)


    def getter(self, obj: Any) -> Callable: # type: ignore
        return getattr(obj, self.callback_accessor)
    
    
    def setter(self, obj: Any, value: Callable[[Any], Any] | None) -> None: # type: ignore
        if value is None:
            return self.deleter(obj)
        
        if not callable(value):
            raise ValueError(f"callback property value must be a callable, not {type(value)}")

        injected = partial(value, obj)
        setattr(obj, self.callback_accessor, injected)
            
        
    def deleter(self, obj: Any) -> None: # type: ignore
        setattr(obj, self.callback_accessor, self.NO_OP)
        
        
        
        
def notify_property_changed(notifier_callback: Callable[[Any, Any], Any] | callback_property) -> type[property]:
    """ Factory decorator for state-change notifier properties. 

        notify_property_changed internally creates and returns a new NotifyPropertyChanged object thats 
        wrapped around a specified notifier_callback, called everytime the underling property state changes.
    """
    
    class NotifyPropertyChanged(property):
        def __init__(self, 
                     fget: Callable[[Any], Any] | None = None, 
                     fset: Callable[[Any, Any], None] | None = None, 
                     fdel: Callable[[Any], None] | None = None, 
                     doc: str | None = None):
            if fset:
                fset = self._setter_wrapper(fset)
                
            super().__init__(fget, fset, fdel, doc)


        def _setter_wrapper(self, fset):
            def inner(obj: Any, value: Any):
                if not self.fget or value != self.fget(obj):
                    if isinstance(notifier_callback, callback_property):
                        callback = notifier_callback.__get__(obj)
                        callback(value)
                    else:
                        notifier_callback(obj, value)
                    
                fset(obj, value)
                
            return inner
        
        
    return NotifyPropertyChanged
        



class EvalAttrProxy(ABC):
    def __init__(self, value: float):
        self.value = value
        
        
    @abstractmethod
    def evaluate(self, obj) -> Any:
        pass
    
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value})"
        