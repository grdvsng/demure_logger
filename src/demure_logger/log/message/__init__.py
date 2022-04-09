import inspect

from .column     import BasicColumn
from typing      import TypeVar, Callable, List, Generic, Optional, Iterable, overload
from .exceptions import LineWrongAttributeType, ColumnDoesntExists


MessageColumn = TypeVar( 'MessageColumn', bound=BasicColumn )
T             = TypeVar( 'T' )


class BasicMessage( Generic[T] ):
    __formater__: Callable[ ..., T ]
    __ordered__ : Iterable[MessageColumn]

    __columns__ : List[ MessageColumn ]

    def __init__( self, 
        formater: Callable[ ..., T ] = lambda columns: [ column.render( ) for column in columns ],
        sort_by:  Optional[ Iterable[str] | Callable[ [ MessageColumn ], int|str ] ] = None,
        **columns_values ):
        self.__columns__ = [ ]

        columns = [
            value for name, value in inspect.getmembers( self, lambda attr: not inspect.isroutine( attr ) )
            if not name.startswith( '_' )
        ]
        
        for column in columns:
            if not isinstance( column, BasicColumn ):
                raise LineWrongAttributeType( f"'{ type( column ) }' is incorrect for Line" )
            elif column.name in columns_values.keys( ):
                column.value = columns_values.get( column.name )

            self.__columns__.append( column )

        self.__formater__ = formater

        columns = [ column for column in self.__columns__ ]

        if sort_by is None:
            self.__ordered__ = columns
        else:
            if callable( sort_by ):
                self.__ordered__ = sorted( columns, key=sort_by )
            else:
                self.__ordered__ = sorted( columns, key=lambda column: sort_by.index( column.name ) )

    def render( self ) -> T:
        return self.__formater__( self.__ordered__ )

    def __repr__( self ) -> str:
        return str( self.render( ) )

    def __str__( self ) -> str:
        return self.__repr__( )

    @overload
    def column( self, name: str ) -> T: ...
    
    @overload
    def column( self, name: str, value: T ) -> None: ...

    def column( self, *args ) -> None:
        names_collumns = [ column.name for column in self.__columns__ ]
        name           = args[0]

        if len( args ) == 1:
            if name in names_collumns:
                return getattr( self, name ).render( )
            else:
                raise ColumnDoesntExists( f"'name' doesn't exists in line" )
        else:
            value          = args[1]
            names_collumns = [ column.name for column in self.__columns__ ]

            if name in names_collumns:
                getattr( self, name ).value = value
            else:
                raise ColumnDoesntExists( f"'name' doesn't exists in line" )


Message = TypeVar( 'Message', bound=BasicMessage )