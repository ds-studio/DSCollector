"""
Constant types in Python.
"""
__doc__ = """
This is a variation on "Constants in Python" by Alex Martelli, from which the
solution idea was borrowed, and enhanced according suggestions of Zoran Isailovski.

In Python, any variable can be re-bound at will -- and modules don't let you
define special methods such as an instance's __setattr__ to stop attribute
re-binding. Easy solution (in Python 2.1 and up): use an instance as "module"...

In Python 2.1 and up, no check is made any more to force entries in sys.modules
to be actually module objects. You can install an instance object there and take
advantage of its attribute-access special methods (e.g., as in this snippet, to
prevent type rebindings.

Usage:
  import consttype
  consttype.magic = 23    # Bind an attribute to a type ONCE
  consttype.magic = 88    # Re-bind it to a same type again
  consttype.magic = "one" # But NOT re-bind it to another type: this raises consttype._ConstError
  del consttype.magic     # Remove an named attribute
  consttype.__del__()     # Remove all attributes
"""

class Contypes:
    class ContypesError(TypeError):
        pass

    def __repr__(self):
        return "Constant type definitions."

    def __setattr__(self, name, value):
        v = self.__dict__.get(name, value)
        if type(v) is not type(value):
            raise self._ConstTypeError, "Can't rebind %s to %s" % (type(v), type(value))
        self.__dict__[name] = value

    def __del__(self):
        self.__dict__.clear()


import sys

procontypes = Contypes()
sys.modules[__name__] = procontypes

procontypes.PROTO_NET_LOGIN               = 0x00000001L
procontypes.PROTO_NET_LOGIN_RESP          = 0x80000001L
procontypes.PROTO_NET_ACTIVE              = 0x80000002L
procontypes.PROTO_NET_ACTIVE_RESP         = 0x80000002L
procontypes.PROTO_NET_IHOSTMETRICS        = 0x00000003L
procontypes.PROTO_NET_IHOSTMETRICS_RESP   = 0x80000003L
procontypes.PROTO_NET_IEPMETRICS          = 0x00000004L
procontypes.PROTO_NET_IEPMETRICS_RESP     = 0x80000004L
procontypes.PROTO_NET_IMQMETRICS          = 0x00000005L
procontypes.PROTO_NET_IMQMETRICS_RESP     = 0x80000005L
procontypes.PROTO_NET_RHOSTMETRICS_RESP   = 0x00000103L
procontypes.PROTO_NET_REPMETRICS_RESP     = 0x80000103L
procontypes.PROTO_NET_RMQMETRICS          = 0x00000104L
procontypes.PROTO_NET_RMQMETRICS_RESP     = 0x80000104L

procontypes.PROTO_RESP_SUCCSS = 0x00000000L

