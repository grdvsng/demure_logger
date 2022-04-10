import uuid

from datetime                         import datetime
from dateutil.tz                      import tzlocal
from typing                           import Callable, Optional, Generic, Any, Type
from ...types.simple                  import T
from .exceptions                      import FieldValidationError
from ...types                         import get_parent_type_parameter
from ..levels                         import Level, Levels


class Field( Generic[T] ):
    name    : str                 
    default : Optional[ Callable[ [], T ] | T ] 
    type    : Type[T]          
    _value  : T                   

    def __init__( self, 
        name    : Optional[str]                   = None, 
        default : Optional[Callable[ [], T ] | T] = None, 
        value   : Optional[T]                     = None,
    ):        
        self.type   = get_parent_type_parameter( self.__class__, Field )
        self._value = None
        
        if name is None:
            self.name = str( uuid.uuid4( ) )
        else:
            self.name = name

        if value is not None: 
            self.value = value

        self.default = default
    
    def validator( self, value: Any ) -> T:
        if value is None or self.type is None or isinstance( value, self.type ):
            return value
        else:
            raise FieldValidationError( f"Value should be instance of '{self.type}'" )

    @property
    def value( self ) -> Optional[T]:
        value = self._value

        if value is None:
            if callable( self.default ):
                value = self.default(  )
            elif not self.default is None:
                value = self.default
        
        return self.validator( value ) 
    
    @value.setter
    def value( self, value: Optional[T] ):
        self._value = self.validator( value ) 

    def __repr__( self ) -> str:
        return str( self.value )

    def __str__( self ) -> str:
        return self.__repr__( )

    def __eq__( self, other: Any ) -> bool:
        if isinstance( other, self.__class__ ):
            return self.value == other.value
        else:
            return self.value == other


class DatetimeField( Field[datetime] ):
    format = str

    def __init__( self, default: Callable[ [ ], datetime ]=lambda : datetime.now( tzlocal( ) ), format: str='%Y-%m-%d', **kwargs ):
        super( ).__init__( default=default, **kwargs )

        self.format = format

    def __repr__( self ) -> str:
        value = self.value

        return value.strftime( self.format )


NUMBER = int


class NumberField( Field[NUMBER] ): 
    max = Optional[NUMBER]
    min = Optional[NUMBER]

    def __init__( self, max: Optional[NUMBER]=None, min: Optional[NUMBER]=None, **kwargs ):
        self.max = max
        self.min = min 

        super( ).__init__( **kwargs )

    def validator( self, value: Optional[T] ) -> Optional[NUMBER]:
        value = super( ).validator( value ) 

        if value is None:
            return value
        else: 
            if self.max is not None and self.max < value:
                raise FieldValidationError( f"Value can't be greter than {self.max}" )

            if self.min is not None and self.min > value:
                raise FieldValidationError( f"Value can't be less than {self.min}" )

            return value


class LogLevelField( Field[Level] ): ...
  
  
class TextField( Field[str] ):
    max_size: Optional[int]

    def __init__( self, max_size: Optional[int]=None, **kwargs ):
        self.max_size = max_size

        super( ).__init__( **kwargs )

    def validator( self, value: Optional[T] ) -> Optional[str]:
        value = super( ).validator( value )

        if value is None:
            return value
        else: 
            if self.max_size is None:
                return value
            elif len( value ) <= self.max_size:
                return value
            else:
                raise FieldValidationError( f"Max size is '{self.max_size}'" )