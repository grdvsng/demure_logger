from typing                    import TypeVar, Callable, List, Dict, Any
from demure_logger             import BasicLogger
from .message                  import Message
from demure_logger.format.text import Format
from .writer                   import Writer
from demure_logger.log         import Levels, Level


MessageType = TypeVar( 'MessageType', bound=Message )
FormatType  = TypeVar( 'FormatType' , bound=Format  )
WriterType  = TypeVar( 'WriterType' , bound=Writer  )


class Logger( BasicLogger ):
    def __init__( self, 
        writer       : Callable[ ..., WriterType  ] | WriterType  = Writer( ),
        format       : Callable[ ..., FormatType  ] | FormatType  = Format( ),
        message_class: Callable[ ..., MessageType ] | MessageType = Message,
        *args,
        **kwargs
    ):
        super( ).__init__( writer, format, message_class, *args, **kwargs ) 