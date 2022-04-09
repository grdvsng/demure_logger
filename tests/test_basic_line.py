import unittest

from src.demure_logger.writers.basic.line import BasicLine, BasicColumn, LineWrongAttributeType


TEST_COLUMN_1_DEFAULT = lambda : 10 * 10
TEST_COLUMN_1_VALUE   = 100
TEST_COLUMN_2_DEFAULT = lambda : 10 * 130
TEST_COLUMN_2_VALUE   = 1300
TEST_FORMATER         = lambda columns: [ str( column ) for column in columns ]
TEST_FORMATER_NAME    = lambda columns: [   column.name for column in columns ]
TEST_SORTED_ITER      = [ 'column_2', 'column_1' ]
TEST_SORTED_FUNC      = lambda column : TEST_SORTED_ITER.index( column.name )


class Test( unittest.TestCase ):
    def test_create_simple_instance( self ):
        class CorrectLineClass( BasicLine ):
            column_1 = BasicColumn( default=TEST_COLUMN_1_DEFAULT )
            column_2 = BasicColumn( default=TEST_COLUMN_2_DEFAULT )

        instance = CorrectLineClass( )

        self.assertEqual( instance.column_1, TEST_COLUMN_1_VALUE )
        self.assertEqual( instance.column_2, TEST_COLUMN_2_VALUE )

    def test_create_wrong_instance( self ):
        class CorrectLineClass( BasicLine ):
            column_1 = BasicColumn( default=TEST_COLUMN_1_DEFAULT )
            column_2 = BasicColumn( default=TEST_COLUMN_2_DEFAULT )
            column_3 = 123

        self.assertRaises( LineWrongAttributeType, lambda: CorrectLineClass( ) )

    def test_create_line_with_kwargs( self ):
        class CorrectLineClass( BasicLine ):
            column_1 = BasicColumn( )
            column_2 = BasicColumn( )

        instance = CorrectLineClass( column_1=TEST_COLUMN_1_VALUE, column_2=TEST_COLUMN_2_VALUE )

        self.assertEqual( instance.column_1, TEST_COLUMN_1_VALUE )
        self.assertEqual( instance.column_2, TEST_COLUMN_2_VALUE )

    def test_create_line_with_sorted_kwargs( self ):
        class CorrectLineClass( BasicLine ):
            column_1 = BasicColumn( )
            column_2 = BasicColumn( )

        instance = CorrectLineClass( formater=TEST_FORMATER_NAME, sort_by=TEST_SORTED_ITER, column_1=TEST_COLUMN_1_VALUE, column_2=TEST_COLUMN_2_VALUE )

        self.assertListEqual( instance.render( ), TEST_SORTED_ITER )

        instance = CorrectLineClass( formater=TEST_FORMATER_NAME, sort_by=TEST_SORTED_FUNC, column_1=TEST_COLUMN_1_VALUE, column_2=TEST_COLUMN_2_VALUE )

        self.assertListEqual( instance.render( ), TEST_SORTED_ITER )
        
    def test_create_simple_instance( self ):
        class CorrectLineClass( BasicLine ):
            column_1 = BasicColumn( default=TEST_COLUMN_1_DEFAULT )
            column_2 = BasicColumn( default=TEST_COLUMN_2_DEFAULT )

        instance = CorrectLineClass( formater=TEST_FORMATER )
        
        self.assertListEqual( instance.render( ), [ str( TEST_COLUMN_1_VALUE ), str( TEST_COLUMN_2_VALUE ) ] )


if __name__ == '__main__':
    unittest.main( )