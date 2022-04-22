from functools import partial
from typing import Callable


class callbackproperty(property):
    """ Descriptor class for callable properties. 

        callbackproperty makes sure a property is always callable, giving it 
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


    def getter(self, obj: type) -> Callable:
        return getattr(obj, self.callback_accessor)
    
    
    def setter(self, obj: type, value: Callable | None) -> None:
        if value is None:
            return self.deleter(obj)
        
        if not callable(value):
            raise ValueError(f"callback property value must be a callable, not {type(value)}")

        injected = partial(value, obj)
        setattr(obj, self.callback_accessor, injected)
            
        
    def deleter(self, obj: type) -> None:
        setattr(obj, self.callback_accessor, self.NO_OP)
        