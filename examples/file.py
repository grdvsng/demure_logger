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