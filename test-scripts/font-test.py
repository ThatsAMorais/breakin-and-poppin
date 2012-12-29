from types import *
from ui.Font import Font
from ui.UIText import UIText
from managers.FontManager import *

fontMgr = FontManager()
# make the font
aFont = fontMgr.loadFont( 'JohnDoe' )
bFont = fontMgr.loadFont( 'JohnDoe' )

print type(aFont)

# make the text object from the font
aUIText = UIText( value="abcdefghi6789", font=aFont, size=20, pos=[0,0] )

aUIText.setFont( bFont )
