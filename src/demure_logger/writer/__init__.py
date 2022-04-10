from typing import TypeVar, Generic, List
from abc    import abstractmethod


T = TypeVar( 'T' )


class BasicWriter( Generic[T] ):
    def write( self, message: T ) -> None: ...

    def __call__( self, *messages: List[T] ) -> None: 
        for message in messages:
            self.write( message )