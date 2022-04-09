import asyncio 
import unittest

from src.demure_logger.writers.console.colors import controller
from src.demure_logger.writers.console.colors import exceptions
from src.demure_logger.writers.console.colors import decorators


TEST_BACKGROUND = 'yellow' 
TEST_CONTENT    = 'test'
TEST_COLOR      = 'red'
TEST_STYLE      = 'bright'

loop = asyncio.new_event_loop( )

asyncio.set_event_loop( loop )    


class TestConsoleColor( unittest.TestCase ):
    def test_get_code( self ):
        self.assertEqual( controller.get_style( TEST_STYLE ), '\x1b[1m'  )

        self.assertEqual( controller.get_code ( TEST_COLOR            ), '\x1b[31m' )
        self.assertEqual( controller.get_code ( TEST_BACKGROUND, True ), '\x1b[43m' )

    def test_get_code_exception( self ):
        self.assertRaises( exceptions.StyleDoesntExists, lambda : controller.get_style( TEST_STYLE + "_" ) )

        self.assertRaises( exceptions.ColorDoesntExists, lambda : controller.get_code( TEST_COLOR      + '_'       ) )
        self.assertRaises( exceptions.ColorDoesntExists, lambda : controller.get_code( TEST_BACKGROUND + '_', True ) )

    def test_text( self ):
        collored = controller.text( TEST_CONTENT, TEST_COLOR        )
        styled   = controller.text( TEST_CONTENT, TEST_COLOR, TEST_STYLE )

        self.assertNotEqual( TEST_CONTENT, collored )
        
        self.assertNotEqual( collored, styled )

    def test_background( self ):
        collored = controller.background( TEST_CONTENT, TEST_COLOR        )
        styled   = controller.background( TEST_CONTENT, TEST_COLOR, TEST_STYLE )

        self.assertNotEqual( TEST_CONTENT, collored )
        
        self.assertNotEqual( collored, styled )


    def test_paint( self ):      
        collored  = controller.paint( TEST_CONTENT, TEST_COLOR                              )
        collored1 = controller.paint( TEST_CONTENT, TEST_COLOR, TEST_BACKGROUND             )
        styled    = controller.paint( TEST_CONTENT, TEST_COLOR, TEST_BACKGROUND, TEST_STYLE )


        self.assertNotEqual( TEST_CONTENT, collored )
        
        self.assertNotEqual( collored, collored1 )

        self.assertNotEqual( collored1, styled )

    def test_decorators( self ):
        @decorators.paint( TEST_COLOR )
        def collored( ) -> str:
            return TEST_CONTENT
       
        @decorators.paint( TEST_COLOR, TEST_BACKGROUND )
        def collored1( ) -> str:
            return TEST_CONTENT
        
        @decorators.paint( TEST_COLOR, TEST_BACKGROUND, TEST_STYLE )
        def styled( ) -> str:
            return TEST_CONTENT

        self.assertNotEqual( TEST_CONTENT, collored( ) )

        self.assertNotEqual( collored( ), collored1( ) )

        self.assertNotEqual( collored1( ), styled( ) ) 

    def test_decorators_async( self ):
        @decorators.paint( TEST_COLOR )
        async def collored( ) -> str:
            return TEST_CONTENT
       
        @decorators.paint( TEST_COLOR, TEST_BACKGROUND )
        def collored1( ) -> str:
            return TEST_CONTENT
        
        @decorators.paint( TEST_COLOR, TEST_BACKGROUND, TEST_STYLE )
        def styled( ) -> str:
            return TEST_CONTENT

        self.assertNotEqual( TEST_CONTENT,  loop.run_until_complete( collored( ) ) )

        self.assertNotEqual( loop.run_until_complete( collored( ) ), collored1( ) )

        self.assertNotEqual( collored1( ), styled( ) ) 


if __name__ == '__main__':
    unittest.main( )