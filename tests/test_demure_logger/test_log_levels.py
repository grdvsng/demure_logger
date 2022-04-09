import unittest

from src.demure_logger.log            import Levels
from src.demure_logger.log.exceptions import LogLevelsDigestReadOnlyExists, LevelDoesntExists


class TestLogLevels( unittest.TestCase ):
    def test_get( self ):
        self.assertEqual( Levels.ignore, 0 ) 
        self.assertEqual( Levels.fatal , 1 )  
        self.assertEqual( Levels.ignOre, 0 ) 
        self.assertEqual( Levels.fAtal , 1 ) 

        self.assertRaises( LevelDoesntExists, lambda : Levels.test )

    def test_cmp( self ):
        self.assertEqual( Levels.ignore, Levels.ignore )
        self.assertLess ( Levels.ignore, Levels.fatal  )

        self.assertGreater( Levels.fatal , Levels.ignore )

        self.assertRaises( TypeError, lambda : Levels.fatal >= "133" )

    def test_set( self ):
        def _( ) : 
            Levels.test = 123

        self.assertRaises( LogLevelsDigestReadOnlyExists, _ )


if __name__ == '__main__':
    unittest.main( )