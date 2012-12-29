
#####
# Dependencies
PyOpenGL 3.x
PIL

    #host = '130.18.57.16'
    #host = '192.168.1.5'


###############
# Bug Report ##
###############

1.)	Oct 3, 2008:
	
	## Line : engine.GameEngine.In __InitGL__()
	iViewport = glGetIntegerv( GL_VIEWPORT )

	## Solution :
	The line was removed as it was not in use; a useless oversight.
	
	## Traceback ##
	Traceback (most recent call last):
	  File "BnP.pyw", line 16, in <module>
	    engine = GameEngine()
	  File "C:\Users\dwilson\Downloads\CandR\engine\GameEngine.py", line 44, in __in
	it__
	    self._InitGL_()
	  File "C:\Users\dwilson\Downloads\CandR\engine\GameEngine.py", line 99, in _Ini
	tGL_
	    iViewport = glGetIntegerv( GL_VIEWPORT )
	  File "c:\python25\lib\site-packages\pyopengl-3.0.0b6-py2.5.egg\OpenGL\wrapper.
	py", line 1631, in __call__
	    return self.finalise()( *args, **named )
	  File "c:\python25\lib\site-packages\pyopengl-3.0.0b6-py2.5.egg\OpenGL\wrapper.
	py", line 683, in wrapperCall
	    converter( pyArgs, index, self )
	  File "c:\python25\lib\site-packages\pyopengl-3.0.0b6-py2.5.egg\OpenGL\converte
	rs.py", line 195, in __call__
	    return self.arrayType.zeros( self.getSize(pyArgs) )
	  File "c:\python25\lib\site-packages\pyopengl-3.0.0b6-py2.5.egg\OpenGL\arrays\a
	rraydatatype.py", line 98, in zeros
	    return cls.returnHandler().zeros( dims, typeCode or cls.typeConstant )
	  File "c:\python25\lib\site-packages\pyopengl-3.0.0b6-py2.5.egg\OpenGL\arrays\n
	ones.py", line 32, in zeros
	    raise TypeError( """Can't create NULL pointer filled with values""" )
	TypeError: ("Can't create NULL pointer filled with values", 'Failure in cConvert
	er <OpenGL.converters.SizedOutput object at 0x02A43070>', [GL_VIEWPORT], 1, <Ope
	nGL.wrapper.glGetIntegerv object at 0x02A40878>)


