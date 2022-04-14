import unittest

from demure_logger.configuration            import Basic
from demure_logger.configuration.exceptions import InvalideValueType, AttributeIsRequired


class Configuration( Basic ):
    name  : str = 5
    value : int


TEST_VALUE = 10
TEST_NAME  = 'test'


class TestMessageField( unittest.TestCase ):
    def test_create_instance( self ):
        instance = Configuration( value=TEST_VALUE, name=TEST_NAME )

        self.assertEqual( instance.value, TEST_VALUE )
        self.assertEqual( instance.name , TEST_NAME  )

    def test_exceptions( self ):
        instance = Configuration( value=TEST_VALUE, name=TEST_NAME )

        self.assertRaises( AttributeError      , lambda : setattr( instance, 'value', TEST_VALUE )          )
        self.assertRaises( InvalideValueType   , lambda : Configuration( name=TEST_VALUE, value=TEST_NAME ) )
        self.assertRaises( AttributeIsRequired , lambda : Configuration( name=TEST_NAME )                   )



