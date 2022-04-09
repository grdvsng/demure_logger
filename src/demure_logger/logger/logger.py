from typing import Literal
from enum   import Enum


class Levels( Enum ):
    OFF   = 0
    FATAL = 1 	
    ERROR = 2 
    WARN  = 3 	
    INFO  = 4 	
    DEBUG = 5