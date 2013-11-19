# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### /home/laiwang/Documents/repy_tuf/sockettimeout.repy

### THIS FILE WILL BE OVERWRITTEN!
### DO NOT MAKE CHANGES HERE, INSTEAD EDIT THE ORIGINAL SOURCE FILE
###
### If changes to the src aren't propagating here, try manually deleting this file. 
### Deleting this file forces regeneration of a repy translation


from repyportability import *
import repyhelper
mycontext = repyhelper.get_shared_context()
callfunc = 'import'
callargs = []

"""
<Author>
  Justin Cappos, Armon Dadgar
  This is a rewrite of the previous version by Richard Jordan

<Start Date>
  26 Aug 2009

<Description>
  A library that causes sockets to timeout if a recv / send call would
  block for more than an allotted amount of time.

"""


class SocketTimeoutError(Exception):
  """The socket timed out before receiving a response"""


class _timeout_socket():
  """
  <Purpose>
    Provides a socket like object which supports custom timeouts
    for send() and recv().
  """

  # Initialize with the socket object and a default timeout
  def __init__(self,socket,timeout=10, checkintv='fibonacci'):
    """
    <Purpose>
      Initializes a timeout socket object.

    <Arguments>
      socket:
              A socket like object to wrap. Must support send,recv,close, and willblock.

      timeout:
              The default timeout for send() and recv().

      checkintv:
              How often socket operations (send,recv) should check if
              they can run. The smaller the interval the more time is
              spent busy waiting.
    """
    # Store the socket, timeout and check interval
    self.socket = socket
    self.timeout = timeout
    self.checkintv = checkintv


  # Allow changing the default timeout
  def settimeout(self,timeout=10):
    """
    <Purpose>
      Allows changing the default timeout interval.

    <Arguments>
      timeout:
              The new default timeout interval. Defaults to 10.
              Use 0 for no timeout. Given in seconds.

    """
    # Update
    self.timeout = timeout
  
  
  # Wrap willblock
  def willblock(self):
    """
    See socket.willblock()
    """
    return self.socket.willblock()


  # Wrap close
  def close(self):
    """
    See socket.close()
    """
    return self.socket.close()


  # Provide a recv() implementation
  def recv(self,bytes,timeout=None):
    """
    <Purpose>
      Allows receiving data from the socket object with a custom timeout.

    <Arguments>
      bytes:
          The maximum amount of bytes to read

      timeout:
          (Optional) Defaults to the value given at initialization, or by settimeout.
          If provided, the socket operation will timeout after this amount of time (sec).
          Use 0 for no timeout.

    <Exceptions>
      As with socket.recv(), socket.willblock(). Additionally, SocketTimeoutError is
      raised if the operation times out.

    <Returns>
      The data received from the socket.
    """

    # It's worth noting that this fibonacci backoff begins with a 2ms poll rate, and 
    # provides a simple exponential backoff scheme.

    fibonacci_backoff = False
    backoff_cap = 100 # Never use more than 100ms poll rate.

    pre_value = 1.0     # Our iterators for Fibonacci sequence.
    pre_pre_value = 1.0 # 

    # Since we want to be able to initialize with static poll rates (backwards 
    # compatibility) we specify a string if we're using the fibonacci backoff.
    if type(self.checkintv) is str:
      if self.checkintv == 'fibonacci':
        fibonacci_backoff = True

    # Set the timeout if None
    if timeout is None:
      timeout = self.timeout

    # Get the start time
    starttime = getruntime()

    # Block until we can read
    rblock, wblock = self.socket.willblock()
    while rblock:
      # Check if we should break
      if timeout > 0:
        # Get the elapsed time
        diff = getruntime() - starttime

        # Raise an exception
        if diff > timeout:
          raise SocketTimeoutError,"recv() timed out!"

      if fibonacci_backoff:
        # Iterate the sequence once
        sleep_length = pre_value + pre_pre_value
        pre_pre_value = pre_value
        pre_value = sleep_length

        # Make sure we don't exceed maximum backoff.
        if sleep_length > backoff_cap:
          sleep_length = backoff_cap

        # Unit conversion to seconds
        sleep_length = sleep_length / 1000.0

        # Sleep
        sleep(sleep_length)
      else: # Classic functionality.
        # Sleep
        try:
          sleep(float(self.checkintv))
        except:
          sleep(0.1)

      # If available, move to the next value of checkintv.
      

      # Update rblock
      rblock, wblock = self.socket.willblock()

    # Do the recv
    return self.socket.recv(bytes)


  # Provide a send() implementation
  def send(self,data,timeout=None):
    """
    <Purpose>
      Allows sending data with the socket object with a custom timeout.

    <Arguments>
      data:
          The data to send

      timeout:
          (Optional) Defaults to the value given at initialization, or by settimeout.
          If provided, the socket operation will timeout after this amount of time (sec).
          Use 0 for no timeout.

    <Exceptions>
      As with socket.send(), socket.willblock(). Additionally, SocketTimeoutError is
      raised if the operation times out.

    <Returns>
      The number of bytes sent.
    """
    # Set the timeout if None
    if timeout is None:
      timeout = self.timeout

    # Get the start time
    starttime = getruntime()

    # Block until we can write
    rblock, wblock = self.socket.willblock()
    while wblock:
      # Check if we should break
      if timeout > 0:
        # Get the elapsed time
        diff = getruntime() - starttime

        # Raise an exception
        if diff > timeout:
          raise SocketTimeoutError,"send() timed out!"

      # Sleep
      # Since switching to the fibonacci backoff, the nature of 
      # this field has changed. Rather than implement the backoff 
      # for checking block status (seems wasteful) we'll just use 
      # a constant value. Ten ms seems appropriate.
      sleep(0.010)

      # Update rblock
      rblock, wblock = self.socket.willblock()

    # Do the recv
    return self.socket.send(data) 




def timeout_openconn(desthost, destport, localip=None, localport=None, timeout=5):
  """
  <Purpose> 
    Wrapper for openconn.   Very, very similar

  <Args>
    Same as Repy openconn

  <Exception>
    Raises the same exceptions as openconn.

  <Side Effects>
    Creates a socket object for the user

  <Returns>
    socket obj on success
  """

  realsocketlikeobject = openconn(desthost, destport, localip, localport, timeout)

  thissocketlikeobject = _timeout_socket(realsocketlikeobject, timeout)
  return thissocketlikeobject





def timeout_waitforconn(localip, localport, function, timeout=5):
  """
  <Purpose> 
    Wrapper for waitforconn.   Essentially does the same thing...

  <Args>
    Same as Repy waitforconn with the addition of a timeout argument.

  <Exceptions> 
    Same as Repy waitforconn

  <Side Effects>
    Sets up event listener which calls function on messages.

  <Returns>
    Handle to listener.
  """

  # We use a closure for the callback we pass to waitforconn so that we don't
  # have to map mainch's to callback functions or deal with potential race
  # conditions if we did maintain such a mapping. 
  def _timeout_waitforconn_callback(localip, localport, sockobj, ch, mainch):
    # 'timeout' is the free variable 'timeout' that was the argument to
    #  timeout_waitforconn.
    thissocketlikeobject = _timeout_socket(sockobj, timeout)

    # 'function' is the free variable 'function' that was the argument to
    #  timeout_waitforconn.
    return function(localip, localport, thissocketlikeobject, ch, mainch)

  return waitforconn(localip, localport, _timeout_waitforconn_callback)

  
  


# a wrapper for stopcomm
def timeout_stopcomm(commhandle):
  """
    Wrapper for stopcomm.   Does the same thing...
  """

  return stopcomm(commhandle)
  
    


### Automatically generated by repyhelper.py ### /home/laiwang/Documents/repy_tuf/sockettimeout.repy
