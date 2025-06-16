from galileo.logger.batch import GalileoBatchLogger
from galileo.logger.stream import GalileoStreamLogger


class GalileoMeta(type):
    """
    This metaclass is responsible for adding methods from GalileoInterface like classes
    to `GalileoLogger` based on mode, or other parameters.
    """

    def __call__(cls, *args, **kwargs):
        for name in ["start_trace", "conclude", "flush", "async_flush"]:
            if kwargs.get("mode", "streaming") == "streaming":
                setattr(cls, name, getattr(GalileoStreamLogger, "start_trace"))
            else:
                setattr(cls, name, getattr(GalileoBatchLogger, "start_trace"))
        obj = cls.__new__(cls, *args, **kwargs)
        if isinstance(obj, cls):
            cls.__init__(obj, *args, **kwargs)
        return obj
