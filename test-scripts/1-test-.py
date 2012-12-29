from ui.Font import Font
from ui.UIText import UIText
from managers.FontManager import *
from engine.Singleton import *
from managers.FontManager import *
from managers.TextureManager import *
from engine.Screen import *
from players.Cop import *
from players.Robber import *

fontMgr = Singleton(FontManager)


# make the font
aFont = fontMgr.loadFont( 'JohnDoe' )
bFont = fontMgr.loadFont( 'JohnDoe' )

# make the text object from the font
aUIText = UIText( "abcdefghi6789", [0,0], bFont, (224,256) )
# output the image of the text
#aUIText.outputTextImage()


