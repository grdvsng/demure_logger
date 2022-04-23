from demure_loggers.console import Logger as ConsoleLogger, Format


CONSOLE_LOGGER = ConsoleLogger( 
    format=Format(
        "{event}\tpid[{pid}]\t{timestamp}\t{message}\r" 
    )
)

loggers = ( CONSOLE_LOGGER,  )