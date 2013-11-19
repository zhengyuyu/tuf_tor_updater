# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### /home/laiwang/Documents/repy_tuf/time_interface.repy

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
<Program Name>
  time_interface.repy

<Author>
  Eric Kimbrel

<Started>
  Jul 2, 2009

<Purpose>
  Provide a framework to run any implementation of a ntp time service that
  follows the interface provided here.

  Any implementation must provide update method that takes a localport 
  as an argument.

  Implementers will set a mapping to their functions by calling 
  time_register_method

  USE:
  
  To use this module, first make a call to time_updatetime(localport),where
  localport is a valid UDP port that you can send and receive on (note that
  this port may not be used depending on the implementation.)

  Then, to get the actual time, call time_gettime() which will return
  the current time (in seconds).

  time.repy will attempt to use the update method of any impelemntor included.
  If none are included or if they all fail an exception is thrown

"""


# dictionary for time implementers to store their information
# the settime method is passed in for use by implementers
TIME_IMP_DICT = {}

time_query_times = []

class TimeError(Exception):
  pass


def time_register_method(imp_name,update_method):
  """
  <Purpose>
  Allow an implementation to register its update method with time.repy

  <Arguments>
  imp_name, the name or unique abbreviation of the implementation
  update_method, a time update_method
  
  <Exceptions>
  None

   <Returns>
   None
  """
  TIME_IMP_DICT[imp_name] = update_method




def time_updatetime(localport):
  """
   <Purpose>
    Obtains and stores the local time from a subset of NTP servers.
    Attempts to update the time with each implementation provided
    until one succeeds or they all fail

   <Arguments>
    localport:
             The local port that MAY be used when contacting the NTP server(s).
             Consider this port a hint and not a rule.
   
   <Exceptions>
    Exception occurs when all methods fail to updatetime, or no such methods 
    are provided (no mehtods have registered)

   <Side Effects>
    time_settime(currenttime) is called as the sub process of a sub process,
    which adjusts the current time.

   <Returns>
    None.
  """
  exception_list = []
  # try the 'update' function for each implementation, storing exceptions in
  # case of total failure, and exiting the function when any of the 'update'
  # functions succeed.
  for update in TIME_IMP_DICT:
    try:
      TIME_IMP_DICT[update](localport)
    except Exception, e:
      exception_list.append(e)
    else:
      return  # exit when we succeed

  # we failed
  ex_str =''
  for ex in exception_list:
    ex_str+=str(ex)
  ex_str = 'ERROR: failed to update ntp time, '+ex_str
  raise Exception(ex_str)





def time_settime(currenttime):
  """
   <Purpose>
    Sets a remote time as the current time.

   <Arguments>
    currenttime:
               The remote time to be set as the current time.

   <Exceptions>
    None.

   <Side Effects>
    Adjusts the current time.

   <Returns>
    None.
  """

  time_query_times.append((getruntime(), currenttime))






def time_gettime():
  """
   <Purpose>
    Gives the current time in seconds by calculating how much time has elapsed
    since the local time was obtained from an NTP server via the
    time_updatetime(localport) function.

   <Arguments>
    None.

   <Exceptions>
    TimeError when time_updatetime(localport)has not previously been called or 
    when time_updatetime(localport) has any unresolved TimeError exceptions.

   <Side Effects>
    None.

   <Returns>
    Current time in seconds.
  """

  if time_query_times == []:
    raise TimeError, "TimeError: time_query_times is an empty list because it has not been set."

  # otherwise use the most recent data...
  latest_update = time_query_times[-1]

  # first item is the getruntime(), second is NTP time...
  elapsedtimesinceupdate = getruntime() - latest_update[0]

  return latest_update[1] + elapsedtimesinceupdate



# in case you want to change to time since the 1970 (as is common)
time_seconds_from_1900_to_1970 = 2208988800




### Automatically generated by repyhelper.py ### /home/laiwang/Documents/repy_tuf/time_interface.repy
