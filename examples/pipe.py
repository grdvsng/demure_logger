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