import logging

FORMAT = "%(levelname)s - %(asctime)s - %(name)s - %(message)s"
LOG_LEVEL = logging.INFO

def getLogger(name, format=FORMAT, level=LOG_LEVEL):
    """Setup basic logging for appllication

     Parameters
    ----------
    name : str
        Name of the logger. The name is typically a dot-separated hierarchical
        name like a, a.b or a.b.c.d. Choice of these names is entirely up
        to the developer who is using logging.

    format : str, optional
        String representing the logging output format:
        https://docs.python.org/3.5/library/logging.html#logging.Formatter

    level : int, optional
        The numeric values of logging levels are given in the following table:
        https://docs.python.org/3.5/library/logging.html#logging-levels
        Deafaults to INFO (20)
    """
    logging.basicConfig(format=format, level=level)
    return logging.getLogger(name)
