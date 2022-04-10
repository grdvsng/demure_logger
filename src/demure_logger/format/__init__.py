from typing import Generic, TypeVar
from abc    import abstractmethod
from ..log.message import Message


T = TypeVar( 'T' )


class BasicFormat( Generic[T] ):
    def __call__( self, message: Message ) -> T: ...