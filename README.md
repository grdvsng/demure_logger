![example console log](./assets/logo.png)

Light were, flexible and customize logging tools.
__Threads and processes safely__!
Package has many default preset to use after installation. 
But if you need customize your own logger, basic classe make you life better.
Smart decorators help you logging your methods on code and catch errors.
Event handler help you connect your handler and send notification on specific events.
Message and field as Model, create you own generic fields, messages, and format.
Configurate multy logger and handle another formats and levels from one instance.


# Curently avaible

__Loggers presets__
    * [Console Logger](./src/demure_loggers/console/__init__.py)
    * [File Logger   ](./src/demure_loggers/file/__init__.py)
    * [JSON Logger   ](./src/demure_loggers/json/__init__.py)

__Programs__
    * [Pipe handler](./scripts/demure-logger-pipe.py)


__Console Logger__
Debug and monitoring you applications via pretty console logging.
![example console log](./assets/console.example.png)

__Examples__
```python
import os
import uuid
import random
import asyncio

from demure_logger.log              import Levels
from demure_loggers.console         import Logger, Format, Writer
from demure_loggers.console.message import Message, TextField


#? Exmaple basic console logger
logger = Logger( )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.info ( "Test" )
logger.debug( "Test" )

# >> FATAL   Test    7916    2022-04-10 21:23:40.749597+04:00        C:\demure_logger\examples\console.py:18
# >> ERROR   Test    7916    2022-04-10 21:23:40.828191+04:00        C:\demure_logger\examples\console.py:19
# >> WARN    Test    7916    2022-04-10 21:23:40.834189+04:00        C:\demure_logger\examples\console.py:20
# >> INFO    Test    7916    2022-04-10 21:23:40.840193+04:00        C:\demure_logger\examples\console.py:#21
# >> DEBUG   Test    7916    2022-04-10 21:23:40.845190+04:00        C:\demure_logger\examples\console.py:22

#? Example with specific formater
logger = Logger( format=Format( "{event}\tpid[{pid}]\t{timestamp}\t{message}" ) )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.info ( "Test" )
logger.debug( "Test" )

# >> FATAL   pid[7916]       2022-04-10 21:23:40.848506+04:00        Test
# >> ERROR   pid[7916]       2022-04-10 21:23:40.851197+04:00        Test
# >> WARN    pid[7916]       2022-04-10 21:23:40.852485+04:00        Test
# >> INFO    pid[7916]       2022-04-10 21:23:40.853072+04:00        Test
# >> DEBUG   pid[7916]       2022-04-10 21:23:40.854629+04:00        Test

#? Example mwith dynamic generate format
def random_fmt( ) -> str:
    fmt = random.choice( [
        "{event}\tpid[{pid}]",
        "{event}\tpid[{pid}]\t{timestamp}",
        "{event}\tpid[{pid}]\t{timestamp}\t{message}",
    ] )

    return Format( fmt )

logger = Logger( format=random_fmt )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.info ( "Test" )
logger.debug( "Test" )

# >> FATAL   pid[7916]       2022-04-10 21:23:40.856367+04:00
# >> ERROR   pid[7916]       2022-04-10 21:23:40.857366+04:00        Test
# >> WARN    pid[7916]       2022-04-10 21:23:40.858204+04:00        Test
# >> INFO    pid[7916]
# >> DEBUG   pid[7916]

#? Example with custom field with default value as function
os.environ["REMOTE_USER"] = "root"

class CustomMessage( Message ):
    user = TextField( default=lambda: os.environ.get( 'REMOTE_USER' ), color='cyan' )

logger = Logger( message_class=CustomMessage, format=Format( "{event}\tpid[{pid}]\t{user}\t{timestamp}\t{message}" ) )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.info ( "Test" )
logger.debug( "Test" )

# >> FATAL   pid[7916]       root    2022-04-10 21:23:40.861895+04:00        Test
# >> ERROR   pid[7916]       root    2022-04-10 21:23:40.862892+04:00        Test
# >> WARN    pid[7916]       root    2022-04-10 21:23:40.864283+04:00        Test
# >> INFO    pid[7916]       root    2022-04-10 21:23:40.865289+04:00        Test
# >> DEBUG   pid[7916]       root    2022-04-10 21:23:40.866884+04:00        Test

#? Example how use custom writer
class CustomWriter( Writer ):
    def write( self, message ):
        print( f"{message} ::{random.randint( 5, 15 )}" )


logger = Logger( writer=CustomWriter( ) )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.info ( "Test" )
logger.debug( "Test" )
 
# >> FATAL   Test    7916    2022-04-10 21:23:40.871144+04:00        C:\demure_logger\examples\console.py:79 ::7
# >> ERROR   Test    7916    2022-04-10 21:23:40.873586+04:00        C:\demure_logger\examples\console.py:80 ::11
# >> WARN    Test    7916    2022-04-10 21:23:40.880757+04:00        C:\demure_logger\examples\console.py:81 ::6
# >> INFO    Test    7916    2022-04-10 21:23:40.885183+04:00        C:\demure_logger\examples\console.py:82 ::9
# >> DEBUG   Test    7916    2022-04-10 21:23:40.889546+04:00        C:\demure_logger\examples\console.py:83 ::8

#? Example use as decorator
logger = Logger( )

@logger.decorate
def decorated_func( ):
    return random.randint( 1, 10 )

decorated_func( )

# >> DEBUG   15292   2022-04-10 23:05:22.265649+04:00 start 'decorated_func'
# >> DEBUG   15292   2022-04-10 23:05:22.267645+04:00 end 'decorated_func'

@logger.decorate( Levels.info )
def decorated_func( ):
    return random.randint( 1, 10 )

decorated_func( )

# >> INFO    8480    2022-04-10 23:06:46.142603+04:00        start 'decorated_func'
# >> INFO    8480    2022-04-10 23:06:46.146584+04:00        end 'decorated_func'

@logger.decorate( Levels.warn, lambda f: f"{ f.__name__ }\t{ uuid.uuid4( ) }" )
def decorated_func( ):
    return random.randint( 1, 10 )

decorated_func( )

# >> WARN    20376   2022-04-10 23:08:44.777405+04:00        start 'decorated_func   2abf32bb-5176-4dc1-be16-ed5c18179b23'
# >> WARN    20376   2022-04-10 23:08:44.778962+04:00        end 'decorated_func     2abf32bb-5176-4dc1-be16-ed5c18179b23'

@logger.decorate
async def decorated_func( ):
    return random.randint( 1, 10 )


loop = asyncio.new_event_loop( )

asyncio.set_event_loop( loop ) 

loop.run_until_complete( decorated_func( ) )

# >> DEBUG   17436   2022-04-10 23:14:24.882050+04:00        start async decorated_func
# >> DEBUG   17436   2022-04-10 23:14:24.883049+04:00        end async decorated_func

@logger.catch
def decorated_func( ):
    raise Exception( "test" )

try:
    decorated_func( )
except Exception as _:
    ...

# >> WARN    19168   2022-04-10 23:28:34.154133+04:00        test

@logger.catch( Levels.fatal )
def decorated_func( ):
    raise Exception( "test" )

try:
    decorated_func( )
except Exception as _:
    ...


# >> FATAL   19168   2022-04-10 23:28:34.154133+04:00        test
```

__File Logger__
Generic file names, formaters, writers, good solution for serveci logging and debug.

__Example__
```python
import os
import json

from datetime                    import datetime
from demure_logger.log           import Levels
from demure_loggers.file         import Logger, Format, Writer
from demure_loggers.file.message import Message


#? Exmaple basic file logger
logger = Logger( path="./.temp/test.log", level=Levels.DEBUG )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.info ( "Test" )
logger.debug( "Test" )

# << "./.temp/test.log"
# >> FATAL	23644	2022-04-11T11:51:51.499851+0400Z	Test
# >> ERROR	23644	2022-04-11T11:51:51.501831+0400Z	Test
# >> WARN	23644	2022-04-11T11:51:51.507830+0400Z	Test
# >> INFO	23644	2022-04-11T11:51:51.514833+0400Z	Test
# >> DEBUG	23644	2022-04-11T11:51:51.521107+0400Z	Test

#? Exmaple basic file logger with generic path
logger = Logger( 
    path=lambda : os.path.join( "./.temp/", datetime.now( ).strftime( "%Y-%m-%d") + ".log" ), 
    level=Levels.DEBUG 
)

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.info ( "Test" )
logger.debug( "Test" )

# << ./.temp/2022-04-11.log
# >> FATAL	18044	2022-04-11T11:54:40.606960+0400Z	Test
# >> ERROR	18044	2022-04-11T11:54:40.607960+0400Z	Test
# >> WARN	18044	2022-04-11T11:54:40.618964+0400Z	Test
# >> INFO	18044	2022-04-11T11:54:40.628961+0400Z	Test
# >> DEBUG	18044	2022-04-11T11:54:40.635963+0400Z	Test

#? Example load configuration from config
config = f"""{{
    "name"   : "test-log",
    "level"  : "debug"   ,
    
    "message_class": "demure_loggers.file.message.Message",

    "writer" : {{
        "props" : {{ 
            "path": "{ os.path.join( "./.temp/", datetime.now( ).strftime( "%Y-%m-%d" ) + ".log" ) }"
        }} 
    }},
    
    "format" : {{
        "props" : {{
            "format": "{{event}}\\t{{timestamp}}\\t{{message}}" 
        }}
    }}
}}"""

logger = Logger.from_config( json.loads( config ) )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.info ( "Test" )
logger.debug( "Test" )

# << ./.temp/2022-04-11.log
# >> FATAL	18044	2022-04-11T11:54:40.606960+0400Z	Test
# >> ERROR	18044	2022-04-11T11:54:40.607960+0400Z	Test
# >> WARN	18044	2022-04-11T11:54:40.618964+0400Z	Test
# >> INFO	18044	2022-04-11T11:54:40.628961+0400Z	Test
# >> DEBUG	18044	2022-04-11T11:54:40.635963+0400Z	Test

#? from config multi
config = f"""[{{
    "name"   : "test-log-debug",
    "level"  : "debug"   ,
    
    "message_class": "demure_loggers.file.message.OsEnvironMixin",

    "writer" : {{
        "props" : {{ 
            "path": "{ os.path.join( "./.temp/", datetime.now( ).strftime( "%Y-%m-%d" ) + ".full.log" ) }"
        }} 
    }},
    
    "format" : {{
        "props" : {{
            "format": "{{event}}\\t{{timestamp}}\\tuser={{USERNAME}}\\t{{OS}}\\t{{message}}" 
        }}
    }}
}}, {{
    "name"   : "test-log-error",
    "level"  : "error"         ,
    
    "message_class": "demure_loggers.file.message.TraceMixin",

    "writer" : {{
        "props" : {{ 
            "path": "{ os.path.join( "./.temp/", datetime.now( ).strftime( "%Y-%m-%d" ) + ".error.log" ) }"
        }} 
    }},
    
    "format" : {{
        "props" : {{
            "format": "{{event}}\\t{{timestamp}}\\t{{trace}}\\t{{message}}" 
        }}
    }}
}}]"""

logger = Logger.from_config( *json.loads( config ) )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.info ( "Test" )
logger.debug( "Test" )

# << ./.temp/2022-04-11.full.log
# >> FATAL	2022-04-13T19:45:04.353500+0400Z	user=root	Windows_NT	Test
# >> ERROR	2022-04-13T19:45:04.536819+0400Z	user=root	Windows_NT	Test
# >> WARN	2022-04-13T19:45:04.560209+0400Z	user=root	Windows_NT	Test
# >> INFO	2022-04-13T19:45:04.570357+0400Z	user=root	Windows_NT	Test
# >> DEBUG	2022-04-13T19:45:04.580500+0400Z	user=root	Windows_NT	Test


# << ./.temp/2022-04-11.error.log
# >> FATAL	2022-04-13T19:22:16.206387+0400Z	C:\demure_logger\examples\file.py:125	Test
# >> ERROR	2022-04-13T19:22:16.377245+0400Z	C:\demure_logger\examples\file.py:126	Test

#? Multy log via usual config
logger1 = Logger( 
    path=lambda : os.path.join( "./.temp/", datetime.now( ).strftime( "%Y-%m-%d") + ".full.log" ), 
    level=Levels.DEBUG 
)

logger2 = Logger( 
    path=lambda : os.path.join( "./.temp/", datetime.now( ).strftime( "%Y-%m-%d") + ".error.log" ), 
    level=Levels.ERROR 
)

logger = Logger.multy( logger1, logger2 )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.info ( "Test" )
logger.debug( "Test" )


# << ./.temp/2022-04-11.full.log
# >> FATAL	23644	2022-04-11T11:51:51.499851+0400Z	Test
# >> ERROR	23644	2022-04-11T11:51:51.501831+0400Z	Test
# >> WARN	23644	2022-04-11T11:51:51.507830+0400Z	Test
# >> INFO	23644	2022-04-11T11:51:51.514833+0400Z	Test
# >> DEBUG	23644	2022-04-11T11:51:51.521107+0400Z	Test

# << ./.temp/2022-04-11.error.log
# >> FATAL	23644	2022-04-11T11:51:51.499851+0400Z	Test
# >> ERROR	23644	2022-04-11T11:51:51.501831+0400Z	Test

#? Treard safe
import threading

logger = Logger( 
    path="./.temp/test.threading.log", 
    level=Levels.debug 
)

tasks    = [ ]

def info( message ) : 
    return logger.info( message )

for message in range( 5 ):
    task = threading.Thread( target = info, args = ( str( message ), ) )
    
    task.start( )

    tasks.append( task )

for task in tasks: task.join( )

# << ./.temp/test.threading.log
# >> INFO	15976	2022-04-13T22:11:08.282878+0400Z	0
# >> INFO	21180	2022-04-13T22:11:08.282878+0400Z	1
# >> INFO	10456	2022-04-13T22:11:08.282878+0400Z	2
# >> INFO	24328	2022-04-13T22:11:08.282878+0400Z	3
# >> INFO	21112	2022-04-13T22:11:08.292814+0400Z	4

#? Multy fork safe
tasks = [ ]

def info( message ) : 
    logger = Logger( 
        path="./.temp/test.forks.log", 
        level=Levels.debug 
    )
    
    return logger.info( message )

for message in range( 5 ):
    task = threading.Thread( target = info, args = ( str( message ), ) )
    
    task.start( )

    tasks.append( task )

for task in tasks: task.join( )

# << ./.temp/test.threading.log
# >> INFO	12440	2022-04-13T22:13:59.878289+0400Z	0
# >> INFO	21924	2022-04-13T22:13:59.880309+0400Z	1
# >> INFO	3956	2022-04-13T22:13:59.881299+0400Z	2
# >> INFO	21436	2022-04-13T22:13:59.882290+0400Z	3
# >> INFO	11792	2022-04-13T22:13:59.883294+0400Z	4
# >> INFO	7596	2022-04-13T22:14:00.002828+0400Z	0
# >> INFO	10768	2022-04-13T22:14:00.003832+0400Z	1
# >> INFO	24556	2022-04-13T22:14:00.005832+0400Z	2
# >> INFO	17008	2022-04-13T22:14:00.006833+0400Z	3
# >> INFO	20388	2022-04-13T22:14:00.008832+0400Z	4
```

__JSON Logger__
Look like file logging, but more flexible and preferebly if you have some logging analizators or searching engines
![example console log](./assets/json.example.png)

__Examples__
```python
import os
import sys
import socket
import pathlib
import threading
from demure_logger.log           import Levels
from demure_loggers.json         import Logger, Format, Message
from demure_loggers.file.message import TextField

#? Exmaple basic json logger
logger = Logger( path="./.temp/test.log.json", level=Levels.DEBUG )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.debug( "Test" )
logger.info ( "Test" )

# << ./.temp/test.log.json
# >> {
# >>     "records": [
# >>         {
# >>             "event": "INFO",
# >>             "id": "e35cba65-f1ce-4f79-80d7-362eb39371b6",
# >>             "message": "Test",
# >>             "pid": 92,
# >>             "timestamp": "2022-04-14T19:46:41.381391+0400Z"
# >>         },
# >>         {
# >>             "event": "DEBUG",
# >>             "id": "337202b3-7eeb-43fa-9c82-c14515f36c42",
# >>             "message": "Test",
# >>             "pid": 92,
# >>             "timestamp": "2022-04-14T19:46:41.372392+0400Z"
# >>         },
# >>         {
# >>             "event": "WARN",
# >>             "id": "24a88ec4-acf7-4dec-8eb7-e47aa3617d26",
# >>             "message": "Test",
# >>             "pid": 92,
# >>             "timestamp": "2022-04-14T19:46:41.363389+0400Z"
# >>         },
# >>         {
# >>             "event": "ERROR",
# >>             "id": "3ea23de5-5201-43d6-b326-c20b189688e8",
# >>             "message": "Test",
# >>             "pid": 92,
# >>             "timestamp": "2022-04-14T19:46:41.355389+0400Z"
# >>         },
# >>         {
# >>             "event": "FATAL",
# >>             "id": "8d02e249-c517-4077-b248-dc93ca3a9ef6",
# >>             "message": "Test",
# >>             "pid": 92,
# >>             "timestamp": "2022-04-14T19:46:41.352397+0400Z"
# >>         },
# >>         {
# >>             "event": "INFO",
# >>             "id": "36da9ff1-bb05-4a66-b7a3-541a77b2c989",
# >>             "message": "Test",
# >>             "pid": 11852,
# >>             "timestamp": "2022-04-14T19:46:11.855272+0400Z"
# >>         },
# >>         {
# >>             "event": "DEBUG",
# >>             "id": "87980859-d520-49db-89a1-ba86e29ee839",
# >>             "message": "Test",
# >>             "pid": 11852,
# >>             "timestamp": "2022-04-14T19:46:11.847277+0400Z"
# >>         },
# >>         {
# >>             "event": "WARN",
# >>             "id": "d762b670-826e-407e-8139-cfbb3639c525",
# >>             "message": "Test",
# >>             "pid": 11852,
# >>             "timestamp": "2022-04-14T19:46:11.838271+0400Z"
# >>         },
# >>         {
# >>             "event": "ERROR",
# >>             "id": "cb03f2a6-ef1c-490f-aff2-a235ff0dca54",
# >>             "message": "Test",
# >>             "pid": 11852,
# >>             "timestamp": "2022-04-14T19:46:11.827426+0400Z"
# >>         },
# >>         {
# >>             "event": "FATAL",
# >>             "id": "9d7e4c56-62c1-4cad-8365-d5438d61327d",
# >>             "message": "Test",
# >>             "pid": 11852,
# >>             "timestamp": "2022-04-14T19:46:11.822147+0400Z"
# >>         }
# >>     ]
# >> }

#? Exmaple with specific format json logger
logger = Logger( 
    format=Format( 
        record_type=lambda msg: str( msg.id )
    ),
    path="./.temp/test.log.foramted.json", 
    level=Levels.DEBUG )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.debug( "Test" )
logger.info ( "Test" )

# << ./.temp/test.log.foramted.json
# >> {
# >>     "records": {
# >>         "043597fe-ff4a-478f-8298-062fd8b1b3db": {
# >>             "event": "ERROR",
# >>             "id": "043597fe-ff4a-478f-8298-062fd8b1b3db",
# >>             "message": "Test",
# >>             "pid": 11852,
# >>             "timestamp": "2022-04-14T19:46:11.866270+0400Z"
# >>         },
# >>         "21103852-6007-4c11-b4bc-1940108065df": {
# >>             "event": "DEBUG",
# >>             "id": "21103852-6007-4c11-b4bc-1940108065df",
# >>             "message": "Test",
# >>             "pid": 92,
# >>             "timestamp": "2022-04-14T19:46:41.426436+0400Z"
# >>         },
# >>         "33256d6f-2eac-49fa-8c5c-26c336c24d41": {
# >>             "event": "WARN",
# >>             "id": "33256d6f-2eac-49fa-8c5c-26c336c24d41",
# >>             "message": "Test",
# >>             "pid": 92,
# >>             "timestamp": "2022-04-14T19:46:41.412206+0400Z"
# >>         },
# >>         "50da5004-0f89-4921-aee8-552aaf97365d": {
# >>             "event": "DEBUG",
# >>             "id": "50da5004-0f89-4921-aee8-552aaf97365d",
# >>             "message": "Test",
# >>             "pid": 11852,
# >>             "timestamp": "2022-04-14T19:46:11.885270+0400Z"
# >>         },
# >>         "518db91e-1497-4d43-9ab5-ac9d08d4b8db": {
# >>             "event": "FATAL",
# >>             "id": "518db91e-1497-4d43-9ab5-ac9d08d4b8db",
# >>             "message": "Test",
# >>             "pid": 11852,
# >>             "timestamp": "2022-04-14T19:46:11.864272+0400Z"
# >>         },
# >>         "b13359b6-6c3c-42bc-9596-a7d81add72e4": {
# >>             "event": "FATAL",
# >>             "id": "b13359b6-6c3c-42bc-9596-a7d81add72e4",
# >>             "message": "Test",
# >>             "pid": 92,
# >>             "timestamp": "2022-04-14T19:46:41.402374+0400Z"
# >>         },
# >>         "bd65c88f-78e5-41af-9ced-8f7f850fa5d2": {
# >>             "event": "ERROR",
# >>             "id": "bd65c88f-78e5-41af-9ced-8f7f850fa5d2",
# >>             "message": "Test",
# >>             "pid": 92,
# >>             "timestamp": "2022-04-14T19:46:41.402374+0400Z"
# >>         },
# >>         "dfbe34e1-7791-48bc-8951-c7b1f1ae867b": {
# >>             "event": "INFO",
# >>             "id": "dfbe34e1-7791-48bc-8951-c7b1f1ae867b",
# >>             "message": "Test",
# >>             "pid": 92,
# >>             "timestamp": "2022-04-14T19:46:41.437085+0400Z"
# >>         },
# >>         "e4aef0eb-00f5-4c52-93da-4609524b2869": {
# >>             "event": "WARN",
# >>             "id": "e4aef0eb-00f5-4c52-93da-4609524b2869",
# >>             "message": "Test",
# >>             "pid": 11852,
# >>             "timestamp": "2022-04-14T19:46:11.877270+0400Z"
# >>         },
# >>         "ff2c0ef0-8c3e-4f3f-9816-8cedc8a53e03": {
# >>             "event": "INFO",
# >>             "id": "ff2c0ef0-8c3e-4f3f-9816-8cedc8a53e03",
# >>             "message": "Test",
# >>             "pid": 11852,
# >>             "timestamp": "2022-04-14T19:46:11.893271+0400Z"
# >>         }
# >>     }
# >> }


#? Exmaple with specific loginfo json logger and custom message class
class CustomMessage( Message ):
    script = TextField( value=pathlib.Path( sys.argv[0] ).name )


logger = Logger( 
    message_class=CustomMessage,
    format=Format( 
        record_type=lambda msg: str( msg.id ),
        os         = os.environ.get( 'OS' ),
        last_pi    = threading.current_thread( ).ident,
        host       = socket.gethostname,
        address    = lambda : socket.gethostbyname( socket.gethostname( ) )
    ),
    path="./.temp/test.log.foramted.with_info.json", 
    level=Levels.DEBUG )

logger.info ( "Test" )

# << ./.temp/test.log.foramted.with_info.json
# >> {
# >>     "address": "192.168.1.11",
# >>     "host": "DESKTOP-JISCVL4",
# >>     "last_pi": 3356,
# >>     "os": "Windows_NT",
# >>     "records": {
# >>         "8ed1a9ae-fbcc-4e6c-8e79-ea00126f18d3": {
# >>             "event": "INFO",
# >>             "id": "8ed1a9ae-fbcc-4e6c-8e79-ea00126f18d3",
# >>             "message": "Test",
# >>             "pid": 3356,
# >>             "script": "_json.py",
# >>             "timestamp": "2022-04-14T19:59:55.929278+0400Z"
# >>         }
# >>     }
# >> }]

#? Multy log
logger_1 = Logger( 
    message_class=CustomMessage,
    format=Format( 
        record_type=lambda msg: str( msg.id ),
        os         = os.environ.get( 'OS' ),
        last_pi    = threading.current_thread( ).ident,
        host       = socket.gethostname,
        address    = lambda : socket.gethostbyname( socket.gethostname( ) )
    ),
    path="./.temp/test.log.foramted.debug.json", 
    level=Levels.DEBUG )

logger_2 = Logger( 
    path="./.temp/test.log.error.json", 
    level=Levels.ERROR 
)

logger = logger.multy( logger_1, logger_2 )

logger.fatal( "Test" )
logger.error( "Test" )
logger.warn ( "Test" )
logger.debug( "Test" )
logger.info ( "Test" )

# << ./.temp/test.log.foramted.debug.json
# >> {
# >>     "address": "192.168.1.11",
# >>     "host": "DESKTOP-JISCVL4",
# >>     "last_pi": 9424,
# >>     "os": "Windows_NT",
# >>     "records": {
# >>         "489fc39d-108d-40e6-a915-2000c1a87424": {
# >>             "event": "FATAL",
# >>             "id": "489fc39d-108d-40e6-a915-2000c1a87424",
# >>             "message": "Test",
# >>             "pid": 9424,
# >>             "script": "_json.py",
# >>             "timestamp": "2022-04-14T20:02:54.520485+0400Z"
# >>         },
# >>         "92567b88-b4ec-4cc1-b13c-9efe891ead28": {
# >>             "event": "WARN",
# >>             "id": "92567b88-b4ec-4cc1-b13c-9efe891ead28",
# >>             "message": "Test",
# >>             "pid": 9424,
# >>             "script": "_json.py",
# >>             "timestamp": "2022-04-14T20:02:54.565525+0400Z"
# >>         },
# >>         "95f321ca-3487-4f8f-8b5c-cb1e51c6c738": {
# >>             "event": "DEBUG",
# >>             "id": "95f321ca-3487-4f8f-8b5c-cb1e51c6c738",
# >>             "message": "Test",
# >>             "pid": 9424,
# >>             "script": "_json.py",
# >>             "timestamp": "2022-04-14T20:02:54.585553+0400Z"
# >>         },
# >>         "b157c61b-23c6-4c1c-86fc-0b4030e9fbd0": {
# >>             "event": "ERROR",
# >>             "id": "b157c61b-23c6-4c1c-86fc-0b4030e9fbd0",
# >>             "message": "Test",
# >>             "pid": 9424,
# >>             "script": "_json.py",
# >>             "timestamp": "2022-04-14T20:02:54.525501+0400Z"
# >>         },
# >>         "df28e2fb-c4c1-4354-9b18-a98055466756": {
# >>             "event": "INFO",
# >>             "id": "df28e2fb-c4c1-4354-9b18-a98055466756",
# >>             "message": "Test",
# >>             "pid": 9424,
# >>             "script": "_json.py",
# >>             "timestamp": "2022-04-14T20:02:54.604020+0400Z"
# >>         }
# >>     }
# >> }

# << ./.temp/test.log.error.json
# >> {
# >>     "records": [
# >>         {
# >>             "event": "ERROR",
# >>             "id": "cfd6e0cd-8585-4fff-8006-af67aed8d616",
# >>             "message": "Test",
# >>             "pid": 9424,
# >>             "timestamp": "2022-04-14T20:02:54.545689+0400Z"
# >>         },
# >>         {
# >>             "event": "FATAL",
# >>             "id": "f522dd88-9367-471d-948b-f5604128a596",
# >>             "message": "Test",
# >>             "pid": 9424,
# >>             "timestamp": "2022-04-14T20:02:54.525501+0400Z"
# >>         }
# >>     ]
# >> }

#? Thread safe
tasks  = [ ]
logger = Logger( 
    path="./.temp/test.threard.json", 
    level=Levels.debug 
)

def info( message ) : 
    return logger.info( message )

for message in range( 5 ):
    task = threading.Thread( target = info, args = ( str( message ), ) )
    
    task.start( )

    tasks.append( task )

for task in tasks: task.join( )

# << ./.temp/test.threard.json
# >> {
# >>     "records": [
# >>         {
# >>             "event": "INFO",
# >>             "id": "0ceb54c1-2188-4197-9967-65ff3e37790b",
# >>             "message": "4",
# >>             "pid": 18072,
# >>             "timestamp": "2022-04-14T21:27:20.297679+0400Z"
# >>         },
# >>         {
# >>             "event": "INFO",
# >>             "id": "0a43a0a5-a081-490e-8c00-ffe5e154c026",
# >>             "message": "3",
# >>             "pid": 4264,
# >>             "timestamp": "2022-04-14T21:27:20.297679+0400Z"
# >>         },
# >>         {
# >>             "event": "INFO",
# >>             "id": "94e7e281-b997-4ba2-9c7f-214997dacc4b",
# >>             "message": "2",
# >>             "pid": 1268,
# >>             "timestamp": "2022-04-14T21:27:20.297679+0400Z"
# >>         },
# >>         {
# >>             "event": "INFO",
# >>             "id": "26b72776-39a9-4209-867d-665978baf644",
# >>             "message": "1",
# >>             "pid": 3976,
# >>             "timestamp": "2022-04-14T21:27:20.292607+0400Z"
# >>         },
# >>         {
# >>             "event": "INFO",
# >>             "id": "e5a4b0ca-ae6e-43db-a4c8-625dab0ef9b8",
# >>             "message": "0",
# >>             "pid": 3408,
# >>             "timestamp": "2022-04-14T21:27:20.292607+0400Z"
# >>         }
# >>     ]
# >> }

#? Multy fork safe
tasks = [ ]

def info( message ) : 
    logger = Logger( 
        path="./.temp/test.forks.json", 
        level=Levels.debug 
    )
    
    return logger.info( message )

for message in range( 5 ):
    task = threading.Thread( target = info, args = ( str( message ), ) )
    
    task.start( )

    tasks.append( task )

for task in tasks: task.join( )

# << ./.temp/test.forks.json
# >> {
# >>     "records": [
# >>         {
# >>             "event": "INFO",
# >>             "id": "5c1f8d59-285d-46fa-9244-89637a392820",
# >>             "message": "4",
# >>             "pid": 5160,
# >>             "timestamp": "2022-04-14T21:25:19.387790+0400Z"
# >>         },
# >>         {
# >>             "event": "INFO",
# >>             "id": "b2b77d3d-c934-4872-a5ef-69a4bca5d1e6",
# >>             "message": "3",
# >>             "pid": 13580,
# >>             "timestamp": "2022-04-14T21:25:19.387790+0400Z"
# >>         },
# >>         {
# >>             "event": "INFO",
# >>             "id": "eef128cc-cc8b-430f-9b6c-2ba760e4fdb2",
# >>             "message": "2",
# >>             "pid": 11364,
# >>             "timestamp": "2022-04-14T21:25:19.387790+0400Z"
# >>         },
# >>         {
# >>             "event": "INFO",
# >>             "id": "1551f324-17ec-4c5d-9dd9-6191124740d4",
# >>             "message": "1",
# >>             "pid": 7380,
# >>             "timestamp": "2022-04-14T21:25:19.387790+0400Z"
# >>         },
# >>         {
# >>             "event": "INFO",
# >>             "id": "d9e6b231-d386-4539-a313-207426469614",
# >>             "message": "0",
# >>             "pid": 21908,
# >>             "timestamp": "2022-04-14T21:25:19.387790+0400Z"
# >>         }
# >>     ]
# >> }
```
__PIPE Logger__
It can help you when you debuging your application, need console output and write in some file.

__Examples__
```python
import pathlib
import os
import pathlib


ROOT = str( pathlib.Path( __file__ ).parent.parent )

HANDLER_PATH = os.path.join( ROOT, 'scripts', 'demure-logger-pipe.py' )
TEMP_SCRIPT  = os.path.join( ROOT, '.temp', 'test-program.py' )
TEMP_CONFIG  = os.path.join( ROOT, '.temp', 'test-pipe-config.py' )

with open( TEMP_SCRIPT, 'w' ) as file:
    file.write( '''
import lorem

events = [ "info", "debug", "error", "fatal", "warn" ]

for event in events:
    print( f"{ event } { lorem.sentence( ) }" )
''' )

with open( TEMP_CONFIG, 'w' ) as file:
    file.write('''
import datetime
import pathlib

from os                     import path as os_path
from demure_logger.log      import Levels
from demure_loggers.file    import Logger as FileLogger
from demure_loggers.console import Logger as ConsoleLogger, Format


def FILE_LOG_PATH( ) -> str:
    ymd    = datetime.datetime.now( ).strftime( "%Y-%m-%d" )
    parent = str( pathlib.Path( __file__ ).parent.parent )

    return os_path.join( parent, '.temp', ymd + ".log" )


TEXT_LOGGER = FileLogger(
    path  = FILE_LOG_PATH, 
    level = Levels.DEBUG 
)

CONSOLE_LOGGER = ConsoleLogger( 
    format=Format(
        "{event}\\tpid[{pid}]\\t{timestamp}\\t{message}\\r" 
    )
)

loggers = (
    TEXT_LOGGER,
    CONSOLE_LOGGER,
)
''' )

os.system( f'py {TEMP_SCRIPT} | py {HANDLER_PATH}' )

# << .\.temp\2022-04-23.log
# >> INFO    pid[5588]       2022-04-23 18:45:33.212309+04:00        info Aliquam voluptatem aliquam porro tempora.
# >> DEBUG   pid[5588]       2022-04-23 18:45:33.226306+04:00        debug Aliquam quaerat quiquia aliquam est.
# >> ERROR   pid[5588]       2022-04-23 18:45:33.239302+04:00        error Magnam consectetur eius quisquam velit voluptatem.
# >> FATAL   pid[5588]       2022-04-23 18:45:33.250304+04:00        fatal Aliquam tempora consectetur ipsum.
# >> WARN    pid[5588]       2022-04-23 18:45:33.261305+04:00        warn Magnam numquam neque modi etincidunt sed aliquam sed.

# << console
# >> INFO    pid[5588]       2022-04-23 18:45:33.212309+04:00        info Aliquam voluptatem aliquam porro tempora.
# >> DEBUG   pid[5588]       2022-04-23 18:45:33.226306+04:00        debug Aliquam quaerat quiquia aliquam est.
# >> ERROR   pid[5588]       2022-04-23 18:45:33.239302+04:00        error Magnam consectetur eius quisquam velit voluptatem.
# >> FATAL   pid[5588]       2022-04-23 18:45:33.250304+04:00        fatal Aliquam tempora consectetur ipsum.
# >> WARN    pid[5588]       2022-04-23 18:45:33.261305+04:00        warn Magnam numquam neque modi etincidunt sed aliquam sed.
```