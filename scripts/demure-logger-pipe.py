#! /usr/bin/env python
import os
import sys
import uuid
import asyncio
import pathlib
import importlib.util

from demure_logger.handlers.pipe import Handler, Config


if __name__ == '__main__':
    config_path = os.path.join( os.getcwd( ), 'demure.pipe.config.py' )

    if len( sys.argv ) > 1:
        config_path = sys.argv[1]

    if not os.path.exists( config_path ):
        config_path = os.path.join( 
            str( pathlib.Path( sys.path[0] ).parent ), 
            'config', 
            'demure.pipe.default.config.py' 
        )
    
    spec   = importlib.util.spec_from_file_location( str( uuid.uuid4( ) ), config_path )
    config = importlib.util.module_from_spec( spec )
    
    spec.loader.exec_module( config )
    
    handler = Handler( **Config.from_module( config ) )

    loop = asyncio.new_event_loop( )

    loop.run_until_complete( 
        handler.run( )
    )
   