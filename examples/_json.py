import os
import sys
import socket
import uuid
import pathlib
import threading

sys.path.append( os.path.join( str( pathlib.Path( __file__ ).parent.parent ), 'src' ) ) 

from datetime                    import datetime
from demure_logger.log           import Levels
from demure_loggers.json         import Logger, Format, Writer, Message
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
