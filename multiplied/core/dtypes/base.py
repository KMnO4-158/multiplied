###################
# Object Metadata #
###################
from ... import __version__


class MultipliedMeta:
    """base class for Multiplied types"""
    _dtype = ""
    _soft_type = object()
    _multiplied_version = __version__

    @classmethod
    def _metadata(cls):
        return {
            "soft_type" : cls._soft_type,
            "version": cls._multiplied_version
        }
