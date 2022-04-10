import unittest

from datetime                             import datetime
from demure_logger.log.message.field      import Field, DatetimeField, TextField, NumberField
from demure_logger.log.message.exceptions import FieldValidationError


TEST_COLUMN_NAME        = 'column_1'
TEST_DEFAULT            = 'test'
TEST_DEFAULT_FUNC       = lambda : 10 * 10
TEST_DEFAULT_FUNC_VALUE = 10 * 10
DATETIME_NOW            = datetime.now( )
DATETIME_FORMAT         = '%Y--%m--%d'
TEST_DEFAULT_MAX_SIZE   = 10


class TestMessageField( unittest.TestCase ):
    def test_column_with_name( self ):
        class TEST:
            cls_column = Field( )

        column = Field( name=TEST_COLUMN_NAME )

        self.assertEqual( column.name, TEST_COLUMN_NAME )
    
    def test_column_with_value( self ):
        class TEST:
            cls_column = Field( value=TEST_DEFAULT_FUNC_VALUE )

        column = Field( name=TEST_COLUMN_NAME, value=TEST_DEFAULT_FUNC_VALUE )

        self.assertEqual( column.value, TEST_DEFAULT_FUNC_VALUE )
        self.assertEqual( TEST.cls_column.value, TEST_DEFAULT_FUNC_VALUE )

    def test_column_with_default( self ):
        class TEST:
            cls_column = Field( default=TEST_DEFAULT_FUNC )

        column = Field( name=TEST_COLUMN_NAME, default=TEST_DEFAULT_FUNC )

        self.assertEqual( column.value, TEST_DEFAULT_FUNC_VALUE )
        self.assertEqual( TEST.cls_column.value, TEST_DEFAULT_FUNC_VALUE )

    def test_column_with_formater( self ):
        class TEST:
            cls_column = Field( default=TEST_DEFAULT_FUNC )

        column = Field( name=TEST_COLUMN_NAME, default=TEST_DEFAULT_FUNC )

        self.assertEqual( str( column ), str( TEST_DEFAULT_FUNC_VALUE ) )
        self.assertEqual( str( TEST.cls_column ), str( TEST_DEFAULT_FUNC_VALUE ) )

    def test_datetime_field( self ):
        class TEST:
            cls_column = DatetimeField( value=DATETIME_NOW, format=DATETIME_FORMAT )

        self.assertEqual( str( TEST.cls_column ), str( DATETIME_NOW.strftime( DATETIME_FORMAT ) ) )
        
        def _( ):
            TEST.cls_column.value = '123'

        self.assertRaises( FieldValidationError, _ )

    def test_text_field( self ):
        class TEST:
            cls_column = TextField( value=TEST_DEFAULT, max_size=TEST_DEFAULT_MAX_SIZE )

        self.assertEqual( TEST.cls_column, TEST_DEFAULT )
        
        def _( ):
            TEST.cls_column.value = '*' * ( TEST_DEFAULT_MAX_SIZE + 1 )

        self.assertRaises( FieldValidationError, _ )

    def test_number_field( self ):
        class TEST:
            cls_column = NumberField( min=0, max=TEST_DEFAULT_FUNC_VALUE, value=TEST_DEFAULT_FUNC_VALUE )

        self.assertEqual( TEST.cls_column, TEST_DEFAULT_FUNC_VALUE )

        def _( ):
            TEST.cls_column.value = TEST_DEFAULT_FUNC_VALUE * 2

        self.assertRaises( FieldValidationError, _ )

        
if __name__ == '__main__':
    unittest.main( )