import unittest

from demure_logger.log.message import BasicMessage, Field, MessageWrongFieldType


TEST_COLUMN_1_DEFAULT = lambda : 10 * 10
TEST_COLUMN_1_VALUE   = 100
TEST_COLUMN_2_DEFAULT = lambda : 10 * 130
TEST_COLUMN_2_VALUE   = 1300
TEST_FORMATER         = lambda columns: [ str( column ) for column in columns ]
TEST_FORMATER_NAME    = lambda columns: [   column.name for column in columns ]
TEST_SORTED_ITER      = [ 'column_2', 'column_1' ]
TEST_SORTED_FUNC      = lambda column : TEST_SORTED_ITER.index( column.name )


class TestMessage( unittest.TestCase ):
    def test_create_simple_instance( self ):
        class CorrectLineClass( BasicMessage ):
            column_1 = Field( default=TEST_COLUMN_1_DEFAULT )
            column_2 = Field( default=TEST_COLUMN_2_DEFAULT )

        instance = CorrectLineClass( )

        self.assertEqual( instance.column_1, TEST_COLUMN_1_VALUE )
        self.assertEqual( instance.column_2, TEST_COLUMN_2_VALUE )

    def test_create_wrong_instance( self ):
        class CorrectLineClass( BasicMessage ):
            column_1 = Field( default=TEST_COLUMN_1_DEFAULT )
            column_2 = Field( default=TEST_COLUMN_2_DEFAULT )
            column_3 = 123

        self.assertRaises( MessageWrongFieldType, lambda: CorrectLineClass( ) )

    def test_create_line_with_kwargs( self ):
        class CorrectLineClass( BasicMessage ):
            column_1 = Field( )
            column_2 = Field( )

        instance = CorrectLineClass( column_1=TEST_COLUMN_1_VALUE, column_2=TEST_COLUMN_2_VALUE )

        self.assertEqual( instance.column_1, TEST_COLUMN_1_VALUE )
        self.assertEqual( instance.column_2, TEST_COLUMN_2_VALUE )

    def test_create_line_with_sorted_kwargs( self ):
        class CorrectLineClass( BasicMessage ):
            column_1 = Field( )
            column_2 = Field( )

        instance = CorrectLineClass( sort_by=TEST_SORTED_ITER, column_1=TEST_COLUMN_1_VALUE, column_2=TEST_COLUMN_2_VALUE )

        self.assertListEqual( [ i for i in instance ], [ getattr( instance, i ).value for i in TEST_SORTED_ITER ] )

        instance = CorrectLineClass( formater=TEST_FORMATER_NAME, sort_by=TEST_SORTED_FUNC, column_1=TEST_COLUMN_1_VALUE, column_2=TEST_COLUMN_2_VALUE )

        self.assertListEqual( [ i for i in instance ], [ getattr( instance, i ).value for i in TEST_SORTED_ITER ] )
        
    def test_create_simple_instance( self ):
        class CorrectLineClass( BasicMessage ):
            column_1 = Field( default=TEST_COLUMN_1_DEFAULT )
            column_2 = Field( default=TEST_COLUMN_2_DEFAULT )

        instance = CorrectLineClass( formater=TEST_FORMATER )
        
        self.assertListEqual( [ i for i in instance ], [ TEST_COLUMN_1_VALUE, TEST_COLUMN_2_VALUE ] )

if __name__ == '__main__':
    unittest.main( )