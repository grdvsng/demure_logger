import re
import unittest

from demure_logger.log.message            import BasicMessage
from demure_logger.log.message.exceptions import FieldValidationError
from demure_loggers.console.message.field import TextField


TEST_COLOR      = 'red'
TEST_BACKGROUND = 'blue'
TEST_STYLE      = 'dim'
TEST_VALUE      = 'TEST_VALUE'


class TestMessageField( unittest.TestCase ):
    def test_text_field( self ):
        class Message( BasicMessage ):
            column = TextField( value=TEST_VALUE, max_size=len( TEST_VALUE ), color=TEST_COLOR, background=TEST_BACKGROUND, style=TEST_STYLE )

        self.assertTrue( re.compile( TEST_VALUE ).findall( str( Message.column.value ) ) is not None )

        def _( ):
            Message.column.value = '*' * ( len( TEST_VALUE ) * 2 )

        self.assertRaises( FieldValidationError, _ )

        
if __name__ == '__main__':
    unittest.main( )