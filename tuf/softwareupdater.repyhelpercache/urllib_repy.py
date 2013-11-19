# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### /home/laiwang/Documents/repy_tuf/urllib.repy

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

def urllib_quote(inputstring, safestring="/"):
  """
  <Purpose>
    Encode an inputstring such that it can be used safely in a URL or XML
    document.

  <Arguments>
    inputstring:
           The string to urlencode.

    safestring (optional):
           Specifies additional characters that should not be quoted --
           defaults to "/".

  <Exceptions>
    TypeError if the inputstring or safestring parameters aren't strings.

  <Side Effects>
    None.

  <Returns>
    Urlencoded version of the passed string.
  """

  if type(inputstring) is not str:
    raise TypeError("urllib_quote's inputstring parameter must be a string, not '"+str(type(inputstring))+"'")
  if type(safestring) is not str:
    raise TypeError("urllib_quote's safestring parameter must be a string, not '"+str(type(safestring))+"'")
  

  resultstr = ""

  # We go through each character in the string; if it's not in [0-9a-zA-Z]
  # we wrap it.

  safeset = set(safestring)

  for char in inputstring:
    asciicode = ord(char)
    if (asciicode >= ord("0") and asciicode <= ord("9")) or \
        (asciicode >= ord("A") and asciicode <= ord("Z")) or \
        (asciicode >= ord("a") and asciicode <= ord("z")) or \
        asciicode == ord("_") or asciicode == ord(".") or \
        asciicode == ord("-") or char in safeset:
      resultstr += char
    else:
      resultstr += "%%%02X" % asciicode

  return resultstr




def urllib_quote_plus(inputstring, safestring=""):
  """
  <Purpose>
    Encode a string to go in the query fragment of a URL.

  <Arguments>
    inputstring:
           The string to urlencode.

    safestring (optional):
           Specifies additional characters that should not be quoted --
           defaults to the empty string.

  <Exceptions>
    TypeError if the inputstring or safestring parameters aren't strings.

  <Side Effects>
    None.

  <Returns>
    Urlencoded version of the passed string.
  """

  if type(inputstring) is not str:
    raise TypeError("urllib_quote_plus' inputstring parameter must be a string, not '"+str(type(inputstring))+"'")
  if type(safestring) is not str:
    raise TypeError("urllib_quote_plus' safestring parameter must be a string, not '"+str(type(safestring))+"'")
  

  return urllib_quote(inputstring, safestring + " ").replace(" ", "+")




def urllib_unquote(inputstring):
  """
  <Purpose>
    Unquote a urlencoded string.

  <Arguments>
    inputstring:
           The string to unquote.

  <Exceptions>
    TypeError if the inputstring isn't a string
    ValueError thrown if the last wrapped octet isn't a valid wrapped octet
    (i.e. if the string ends in "%" or "%x" rather than "%xx". Also throws
    ValueError if the nibbles aren't valid hex digits.

  <Side Effects>
    None.

  <Returns>
    The decoded string.
  """

  if type(inputstring) is not str:
    raise TypeError("urllib_unquote's inputstring parameter must be a string, not '"+str(type(inputstring))+"'")
  

  resultstr = ""

  # We go through the inputstring from end to beginning, looking for wrapped
  # octets. When one is found we add it (unwrapped) and the following
  # string to the resultant string, and shorten the original inputstring.

  while True:
    lastpercentlocation = inputstring.rfind("%")
    if lastpercentlocation < 0:
      break

    wrappedoctetstr = inputstring[lastpercentlocation+1:lastpercentlocation+3]
    if len(wrappedoctetstr) != 2:
      raise ValueError("Quoted string is poorly formed")

    resultstr = \
        chr(int(wrappedoctetstr, 16)) + \
        inputstring[lastpercentlocation+3:] + \
        resultstr
    inputstring = inputstring[:lastpercentlocation]

  resultstr = inputstring + resultstr
  return resultstr




def urllib_unquote_plus(inputstring):
  """
  <Purpose>
    Unquote the urlencoded query fragment of a URL.

  <Arguments>
    inputstring:
           The string to unquote.

  <Exceptions>
    TypeError if the inputstring isn't a string
    ValueError thrown if the last wrapped octet isn't a valid wrapped octet
    (i.e. if the inputstring ends in "%" or "%x" rather than "%xx". Also throws
    ValueError if the nibbles aren't valid hex digits.

  <Side Effects>
    None.

  <Returns>
    The decoded string.
  """
  if type(inputstring) is not str:
    raise TypeError("urllib_unquote_plus' inputstring parameter must be a string, not '"+str(type(inputstring))+"'")

  return urllib_unquote(inputstring.replace("+", " "))




def urllib_quote_parameters(inputdictionary):
  """
  <Purpose>
    Encode a dictionary of (key, value) pairs into an HTTP query string or
    POST body (same form).

  <Arguments>
    dictionary:
           The dictionary to quote.

  <Exceptions>
    TypeError if the inputdictionary isn't a dict.

  <Side Effects>
    None.

  <Returns>
    The quoted dictionary.
  """
  if type(inputdictionary) is not dict:
    raise TypeError("urllib_quote_parameters' inputstringdictionary parameter must be a dict, not '"+str(type(inputstring))+"'")

  quoted_keyvals = []
  for key, val in inputdictionary.items():
    quoted_keyvals.append("%s=%s" % (urllib_quote(key), urllib_quote(val)))

  return "&".join(quoted_keyvals)




def urllib_unquote_parameters(inputstring):
  """
  <Purpose>
    Decode a urlencoded query string or POST body.

  <Arguments>
    inputstring:
           The string to decode.

  <Exceptions>
    TypeError if the inputstring isn't a string
    ValueError if the inputstring is poorly formed.

  <Side Effects>
    None.

  <Returns>
    A dictionary mapping keys to values.
  """

  if type(inputstring) is not str:
    raise TypeError("urllib_unquote_parameters' inputstring parameter must be a string, not '"+str(type(inputstring))+"'")

  keyvalpairs = inputstring.split("&")
  res = {}

  for quotedkeyval in keyvalpairs:
    # Throw ValueError if there is more or less than one '='.
    quotedkey, quotedval = quotedkeyval.split("=")
    key = urllib_unquote_plus(quotedkey)
    val = urllib_unquote_plus(quotedval)
    res[key] = val

  return res

### Automatically generated by repyhelper.py ### /home/laiwang/Documents/repy_tuf/urllib.repy
