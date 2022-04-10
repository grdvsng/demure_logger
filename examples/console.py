import os
import sys
import uuid
import uvicorn
import pathlib
import asyncio

sys.path.append( os.path.join( str( pathlib.Path( __file__ ).parent.parent ), 'src' ) ) 


import random

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

#? Use ase service
app = logger.as_service( )
 
uvicorn.run( app )

# > INFO    3828    2022-04-11 00:17:23.846489+04:00        mtnynytrnrrnty
# > INFO:     127.0.0.1:58197 - "POST /Logger HTTP/1.1" 200 OK