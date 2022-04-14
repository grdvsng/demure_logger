import unittest

from demure_logger.format.text import Format
from demure_logger.log.message import Message


class TestTextFormat( unittest.TestCase ):
    def test_formater( self ):
        formater = Format( "{event}\tpid[{pid}]" )
        message  = Message( )

        self.assertEqual( formater(  Message( ) ), f"{message.event}\tpid[{message.pid}]" )
        self.assertEqual( Format( )( Message( ) ), f"{message.event}\t{message.message}\t{message.pid}" )


if __name__ == '__main__':
    unittest.main( )