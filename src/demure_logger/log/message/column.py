import re
import inspect

from typing          import Callable, Optional, Generic, Any, TypeVar
from ...types.simple import T
from .exceptions     import CantGetColumnNameFromScope


FormatedColumn = TypeVar( 'FormatedColumn' )


class BasicColumn( Generic[T] ):
    name    : str                 
    default : Optional[Callable[ [], T ] | T] 
    formater: Callable[ [ T ], FormatedColumn | T ]          
    value   : Optional[T]                     

    def __init__( self, 
        name    : Optional[str]                         = None, 
        default : Optional[Callable[ [], T ] | T]       = None, 
        formater: Callable[ [ T ], FormatedColumn | T ] = lambda value: value, 
        value   : Optional[T]                           = None 
    ):        
        try:
            cls_column_name = inspect.getouterframes( inspect.currentframe( ), 2 )[1][4][1].split( '=' )

            if len( cls_column_name ) < 2:
                cls_column_name = None
            else:
                cls_column_name = cls_column_name[0].strip( )
        except Exception as _:
            cls_column_name = None
        
        if name is None:
            if cls_column_name is None:
                raise CantGetColumnNameFromScope( "Cant get column name from scope" )
            else:
                self.name = cls_column_name
        else:
            self.name = name

        self.formater = formater

        if value is None:
            self.value = None
        else:
            self.value = value

        self.default = default
        
    def render( self ) -> FormatedColumn | T:
        value = self.value

        if value is None:
            if callable( self.default ):
                value = self.default(  )
            elif not self.default is None:
                value = self.default

        return self.formater( value )

    def __repr__( self ) -> str:
        return str( self.render( ) )

    def __str__( self ) -> str:
        return self.__repr__( )

    def __eq__( self, other: Any ) -> bool:
        if isinstance( other, self.__class__ ):
            return self.render( ) == other.render( )
        else:
            return self.render( ) == other
