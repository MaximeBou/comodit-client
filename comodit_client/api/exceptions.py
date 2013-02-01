# coding: utf-8
"""
Provides common API exceptions.
"""

class PythonApiException(Exception):
    """
    Base class for exceptions raised by API calls.
    """

    def __init__(self, message):
        """
        Creates a PythonApiException instance.

        @param message: A message
        @type message: string
        """

        super(PythonApiException, self).__init__(message)
