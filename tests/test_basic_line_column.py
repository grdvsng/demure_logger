import unittest

from src.demure_logger.writers.basic.line.column     import BasicColumn
from src.demure_logger.writers.basic.line.exceptions import CantGetColumnNameFromScope


TEST_COLUMN_NAME        = 'column_1'
TEST_DEFAULT            = 'test'
TEST_DEFAULT_FUNC       = lambda : 10 * 10
TEST_DEFAULT_FUNC_VALUE = 10 * 10
TEST_DEFAULT_FORMATER   = lambda x: str( x )


class Test( unittest.TestCase ):
    def test_column_with_name( self ):
        class TEST:
            cls_column = BasicColumn( )

        column = BasicColumn( name=TEST_COLUMN_NAME )

        self.assertEqual( column.name, TEST_COLUMN_NAME )
        self.assertEqual( TEST.cls_column.name, 'cls_column' )

        self.assertRaises( CantGetColumnNameFromScope, lambda: setattr( TEST, TEST_COLUMN_NAME, BasicColumn( ) ) )
    
    def test_column_with_value( self ):
        class TEST:
            cls_column = BasicColumn( value=TEST_DEFAULT_FUNC_VALUE )

        column = BasicColumn( name=TEST_COLUMN_NAME, value=TEST_DEFAULT_FUNC_VALUE )

        self.assertEqual( column.value, TEST_DEFAULT_FUNC_VALUE )
        self.assertEqual( TEST.cls_column.value, TEST_DEFAULT_FUNC_VALUE )

    def test_column_with_default( self ):
        class TEST:
            cls_column = BasicColumn( default=TEST_DEFAULT_FUNC )

        column = BasicColumn( name=TEST_COLUMN_NAME, default=TEST_DEFAULT_FUNC )

        self.assertEqual( column.render( ), TEST_DEFAULT_FUNC_VALUE )
        self.assertEqual( TEST.cls_column.render( ), TEST_DEFAULT_FUNC_VALUE )

    def test_column_with_formater( self ):
        class TEST:
            cls_column = BasicColumn( default=TEST_DEFAULT_FUNC, formater=TEST_DEFAULT_FORMATER )

        column = BasicColumn( name=TEST_COLUMN_NAME, default=TEST_DEFAULT_FUNC, formater=TEST_DEFAULT_FORMATER )

        self.assertEqual( str( column ), str( TEST_DEFAULT_FUNC_VALUE ) )
        self.assertEqual( str( TEST.cls_column ), str( TEST_DEFAULT_FUNC_VALUE ) )

if __name__ == '__main__':
    unittest.main( )