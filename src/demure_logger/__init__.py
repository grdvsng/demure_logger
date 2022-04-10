import inspect

from fastapi     import FastAPI, Form
from .writer     import BasicWriter
from .format     import BasicFormat
from typing      import TypeVar, Type, Dict, Any, Callable, ParamSpec, List, Tuple, Optional
from .log        import BasicMessage
from .log.levels import Levels, Level
from functools   import wraps


Writer  = TypeVar  ( 'Writer' , bound=BasicWriter  )
Format  = TypeVar  ( 'Format' , bound=BasicFormat  ) 
Message = TypeVar  ( 'Message', bound=BasicMessage )
T       = TypeVar  ( 'T' )
P       = ParamSpec( 'P' )
R       = TypeVar  ( 'R' )


def call_if_callable( instance: Callable[ ..., T ] | T, *args, **kwargs ) -> T:
    if inspect.isfunction( instance ):
        return instance( *args, **kwargs )
    else:
        return instance

MessageDataType = Dict[ str, Any ] | str


class BasicLogger:
    _writer        : Writer        | Callable[ ..., Writer        ]
    _format        : Format        | Callable[ ..., Format        ]
    _message_class : Type[Message] | Callable[ ..., Type[Message] ]
    _level         : Level
    
    def __init__( self, 
        writer        : Writer        | Callable[ ..., Writer        ],
        format        : Format        | Callable[ ..., Format        ],
        message_class : Type[Message] | Callable[ ..., Type[Message] ],
        level         : Level                               =Levels.debug,
        name          : Optional[str] = None,
        event_Hanler  : Callable[ [ Level, Message ], None ]=lambda level, message: ...
    ):
        self.name           = self.__class__.__name__ if name is None else name
        self._writer        =  writer                
        self._format        =  format                 
        self._message_class =  message_class 

        self.level        = level
        self.event_Hanler = event_Hanler
    
    @property
    def writer( self ) -> Writer: return call_if_callable( self._writer )

    @property
    def format( self ) -> Format: return call_if_callable( self._format )

    @property
    def message_class( self ) -> Type[Message]: return call_if_callable( self._message_class )

    def _write( self, event: Level, *messages: List[MessageDataType] ) -> List[Message]:
        result = [ ]
 
        for message in messages:
            message = self.message_class( event=event, **message ) if isinstance( message, dict ) else self.message_class( event=event, message=message )
          
            if event <= self.level:
                formated = self.format.prepare( message )

                self.event_Hanler( event, message )
                
                self.writer.write( formated )
            
            result.append( message )

        return result

    def off( self ):
        self.level = Levels.IGNORE

    def fatal( self, *messages: List[MessageDataType] ):
        return self._write( Levels.fatal, *messages )
    
    def error( self, *messages: List[MessageDataType] ):
        return self._write( Levels.error, *messages )

    def warn( self, *messages: List[MessageDataType] ):
        return self._write( Levels.warn, *messages )

    def info( self, *messages: List[MessageDataType] ):
        return self._write( Levels.info, *messages )

    def debug( self, *messages: List[MessageDataType] ):
        return self._write( Levels.debug, *messages )

    def fatal( self, *messages: List[MessageDataType] ):
        return self._write( Levels.fatal, *messages )

    def decorate( self, 
        *args: Tuple[ Level, Callable[ [ Type[Callable] ], str ] ] | Tuple[ Callable[ P, R ] ]
    ):
        event       = Levels.debug
        func_format = lambda f: f.__name__ 

        if len( args ) > 1 or not callable( args[0] ):
            if len( args ) > 0 and args[0] is not None: event       = args[0]
            if len( args ) > 1 and args[1] is not None: func_format = args[1]

        def wrap( func: Callable[ P, R ] ) -> Callable[ P, R ]:
            formated = func_format( func )

            @wraps( func )
            def __( *args: P.args, **kwargs: P.kwargs ) -> R:
                self._write( event, f"start {formated}" )
                
                result = func( *args, **kwargs )

                self._write( event, f"end {formated}" )

                return result

                        
            @wraps( func )
            async def __async( *args: P.args, **kwargs: P.kwargs ) -> R:
                self._write( event, f"start async {formated}" )
                
                result = await func( *args, **kwargs )

                self._write( event, f"end async {formated}" )

                return result

            return __async if inspect.iscoroutinefunction( func ) else __
        
        return wrap( args[0] ) if len( args ) == 1 and callable( args[0] ) else wrap

    def catch( self, 
        *args: Tuple[ Level, Callable[ [ Exception ], str ] ] | Tuple[ Callable[ P, R ] ]
    ):
        event        = Levels.warn
        error_format = lambda error: f"{error}" 

        if len( args ) > 1 or not callable( args[0] ):
            if len( args ) > 0 and args[0] is not None: event        = args[0]
            if len( args ) > 1 and args[1] is not None: error_format = args[1]

        def wrap( func: Callable[ P, R ] ) -> Callable[ P, R ]:
            @wraps( func )
            def __( *args: P.args, **kwargs: P.kwargs ) -> R:
                try:                   
                    return func( *args, **kwargs )
                except Exception as error:
                    self._write( event, error_format( error ) )

                    raise error
           
            @wraps( func )
            async def __async( *args: P.args, **kwargs: P.kwargs ) -> R:
                try:                   
                    return await func( *args, **kwargs )
                except Exception as error:
                    self._write( event, error_format( error ) )

                    raise error

            return __async if inspect.iscoroutinefunction( func ) else __
        
        return wrap( args[0] ) if len( args ) == 1 and callable( args[0] ) else wrap

    def as_service( self, prefix: Optional[str]=None ) -> FastAPI:
        MessageType = self.message_class.pydantic_type( )
        app         = FastAPI( )
        
        if prefix is None:
            prefix = '/' + self.name

        async def create( level: str = Form( Levels.info.name ), message: str = Form( ... ) ):
            return MessageType( **self._write( getattr( Levels, level ), message )[0].__dict__ )
        
        app.post( prefix, response_model=MessageType )( create )

        return app