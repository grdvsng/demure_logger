import asyncio
import unittest

from demure_logger.structure.queue import Queue
from demure_logger.handlers.basic  import Handler, Event
from demure_loggers.console        import Logger
from demure_logger.log.levels      import Levels


TEST_LOGGER = Logger( )
TEST_QUEUE  = Queue( )
TEST_EVENT  = Event( Levels.INFO, "TEST" )


class TestBasicHandler( unittest.IsolatedAsyncioTestCase ):
    def test_create_instance( self ):
        self.assertIsNotNone( Handler( [ TEST_LOGGER ], TEST_QUEUE ) )

    async def test_handle_event( self ):
        handler = Handler( [ TEST_LOGGER ], TEST_QUEUE )

        await TEST_QUEUE.put( TEST_EVENT )

        await handler.run( 10 )


if __name__ == '__main__':
    unittest.main( )