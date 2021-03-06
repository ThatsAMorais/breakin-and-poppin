#####      File : CommFunctions.py
####	 Author : Alex Morais
### Description : These are functions which both client and server use
###		to both send and receive transmissions between one
###		another.
##

import socket, select, pickle, sys, time

def recvData(channel):
    """
    Receive data from the client and give return it to the server
    """
    clientData = None

    try:
	inData = channel.recv(5048)
	clientData = pickle.loads( inData )
    except (socket.error, socket.herror):
	# if the socket closed (i.e. connection reset by peer)
	#   generate a packet to tell the recipient
	clientData = { 'type' : 'message', 'CRbP' : None } 
    except pickle.UnpicklingError:
	print 'Recv error - unpickling error'
    except ( KeyError
	    , IndexError
	    , EOFError
	    , ImportError
	    , AttributeError
	    , ValueError ):
    	#print 'Recv error - ', sys.exc_info()[1]
    	# for some damn reason I get this err often in packets.
    	#   I'm choosing to ignore them because packets are cheap.
	# I should try and figure out the cause of these errors, but
	#   since things work most of the time I am going to ignore
	#   these issues cautiously
	#print 'RECV-FAILURE:', sys.exc_info()[1], '- The packet size is too small'
	pass

    return clientData


def sendData(channel, packet):
    """
    Sends data to a single client once
    """
    try:
	channel.send( pickle.dumps( packet ) )
    except socket.error:
	print 'SendData - Error sending to client'
    except pickle.PicklingError:
	print 'SendData - PicklingError', sys.exc_info()[1]
	pass

