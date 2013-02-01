# coding: utf-8
"""
Provides classes related to file entities, in particular L{HasFiles}.
"""

from comodit_client.util.json_wrapper import JsonWrapper
from comodit_client.api.collection import Collection
from comodit_client.api.entity import Entity


class Delimiter(JsonWrapper):
    """
    A delimiter is associated to a L{File} and represents the strings that
    have to be put before and after variable names in file's content. For
    instance, default delimiter start is '${' and default delimiter end is
    '}', therefore a file containing a variable called 'foo' will contain
    the following string: '${foo}'.
    """

    @property
    def start(self):
        """
        Delimiter's start.

        @rtype: string
        """

        return self._get_field("start")

    @start.setter
    def start(self, start):
        """
        Sets delimiter's start.

        @param start: Delimiter's start.
        @type start: string
        """

        self._set_field("start", start)

    @property
    def end(self):
        """
        Delimiter's end.

        @rtype: string
        """

        return self._get_field("end")

    @end.setter
    def end(self, end):
        """
        Sets delimiter's end.

        @param end: Delimiter's end.
        @type end: string
        """

        self._set_field("end", end)

    def show(self, indent = 0):
        """
        Prints delimiter's representation to standard output in a user-friendly way.

        @param indent: The number of spaces to put in front of each displayed
        line.
        @type indent: int
        """

        print " "*indent, "Start:", self.start
        print " "*indent, "End:", self.end


class FileEntity(Entity):
    """
    Base class of file entities. This class provides helpers used to set a
    remote file entity's content.
    """

    @property
    def content_url(self):
        """
        URL to remote file's content.

        @rtype: string
        """

        return self.url + "content"

    def set_content(self, path):
        """
        Uploads the content of given local file.

        @param path: Path to local file.
        @type path: string
        """

        self._http_client.upload_to_exising_file_with_path(path, self.content_url)

    def get_content(self):
        """
        Downloads the content of file. The returned value is a file-like object
        like returned by C{urllib2.urlopen}.

        @return: a reader to file's content.
        @rtype: file-like object
        """

        return self._http_client.read(self.content_url, decode = False)


class File(FileEntity):
    """
    File entity representation. A file is the representation of a template.
    The template may be rendered after values are assigned to its variables
    (see U{ComodIT documentation<http://www.comodit.com/entities/api/rendering.html>}).
    """

    @property
    def delimiter(self):
        """
        File's delimiter.

        @rtype: L{Delimiter}
        """

        return Delimiter(self._get_field("delimiter"))

    @delimiter.setter
    def delimiter(self, delim):
        """
        Sets file's delimiter.

        @param delim: File's delimiter.
        @type delim: L{Delimiter}
        """

        self._set_field("delimiter", delim)

    def _show(self, indent = 0):
        print " "*indent, "Name:", self.name
        print " "*indent, "Delimiter:"
        self.delimiter.show(indent + 2)


class FileCollection(Collection):
    """
    Collection of files.

    @see: L{Distribution}, L{Platform}
    """

    def _new(self, json_data = None):
        res = File(self, json_data)
        return res

    def new(self, name):
        """
        Instantiates a new file object.

        @param name: The name of new file.
        @type name: string
        @rtype: L{File}
        """

        f = self._new()
        f.name = name
        return f

    def create(self, name):
        """
        Creates a remote file entity and returns associated local
        object.

        @param name: The name of new distribution.
        @type name: string
        @rtype: L{File}
        """

        f = self.new(name)
        f.create()
        return f


class HasFiles(Entity):
    """
    Super class for entities having files.
    """

    def files(self):
        """
        Instantiates a collection of files.

        @rtype: L{FileCollection}
        """

        return FileCollection(self.client, self.url + "files/")

    def add_file(self, f):
        """
        Adds a file to local list of files. Note that this list is considered only at creation time.
        For later modifications, collection must be used.
        
        @param f: the file to add.
        @type f: L{File}
        """

        self._add_to_list_field("files", f)

    @property
    def files_f(self):
        """
        The local list of files. The object of the list may be used to interact
        with server.

        @rtype: list of L{File}
        """

        return self._get_list_field("files", lambda x: File(self.files(), x))

    @files_f.setter
    def files_f(self, files):
        """
        Sets the list of files. Note that if the remote entity owning the files
        already exists, this operation will have no effect. In order to update
        files, they should be accessed through collection.

        @param files: The new list of files.
        @type files: list of L{File}
        """

        self._set_list_field("files", files)

    def get_file(self, name):
        """
        Fetches a remote file entity given its name.
        
        @param name: The name of the file.
        @type name: string
        """

        return self.files().get(name)

    def _show_files(self, indent = 0):
        print " "*indent, "Files:"
        for s in self.files_f:
            s._show(indent + 2)
