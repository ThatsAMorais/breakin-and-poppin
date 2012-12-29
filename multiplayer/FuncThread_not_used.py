#####      File : FuncThread.py
####	 Author : Alex Morais
### Description : A thread that executes a function and stores the
###		return value of the function where it can be retrieved
###		by the object that 
##
###  This is code that I borrowed from an open online source,
### originally called "Future()", but I didn't like that name
### so I changed it.

from threading import *
import copy, sys

class FuncThread:
    """
    An object that allows a function to be executed in a separate 
    thread.
    """

    def __init__(self,func,*param):
        # Constructor
        self.__done=0
        self.__result=None
	self.__excpt = None
        self.__status='working'

        self.__C=Condition()   # Notify on this Condition when result is ready

        # Run the actual function in a separate thread
        self.__T=Thread(target=self.Wrapper,args=(func,param))
        self.__T.setName("FuncThread")
        self.__T.start()

    def __repr__(self):
        return '<FuncThread at '+hex(id(self))+':'+self.__status+'>'

    def __call__(self):
        self.__C.acquire()
        while self.__done==0:
            self.__C.wait()
        self.__C.release()
	
	# an exception was thrown in the thread, re-raise it here.
	if self.__excpt:
	    raise self.__excpt[0], self.__excpt[1], self.__excpt[2]

        # We deepcopy __result to prevent accidental tampering with it.
        a=copy.deepcopy(self.__result)
        return a

    def Wrapper(self, func, param):
        # Run the actual function, and let us housekeep around it
        self.__C.acquire()
        try:
            self.__result=func(*param)
        except:
            self.__result="Exception raised within FuncThread"
	    self.__excpt = sys.exc_info()
	
        self.__done=1
        self.__status=`self.__result`
        self.__C.notify()
        self.__C.release()

    def isDone(self):
	return self.__done

