# rest.client - Generic client for crud opetations in a REST-Json API.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import urllib, urllib2, json, urlparse
import comodit_client.util.fileupload as fileupload
from urllib2 import HTTPError
from comodit_client.util import urllibx
from comodit_client.rest.exceptions import ApiException


class HttpClient(object):
    def __init__(self, endpoint, username, password, insecure_upload = False):
        self.endpoint = endpoint.rstrip('/')
        self.username = username
        self.password = password
        self._insecure_upload = insecure_upload

    def create(self, entity, item = None, parameters = {}, decode = True):
        url = self._encode_url(entity, parameters)

        if not item is None:
            try:
                json_data = json.dumps(item)
            except Exception, e:
                raise ApiException("Could not encode given data: " + e.message, 0)
            req = self._new_request_with_data(url, "POST", json_data)
        else:
            req = self._new_request(url, "POST")
            # Fix regarding Nginx not supporting empty requests with no
            # Content-Length
            req.add_header("Content-Length", 0)
        raw = self._urlopen(req)
        if decode:
            try:
                return json.load(raw)
            except:
                raise ApiException("Could not decode response: " + raw.read(), 0)
        else:
            return raw

    def read(self, entity, parameters = {}, decode = True):
        url = self._encode_url(entity, parameters)
        req = self._new_request(url, "GET")
        raw = self._urlopen(req)
        if decode:
            return json.load(raw)
        else:
            return raw

    def update(self, entity, item = None, parameters = {}, decode = True):
        url = self._encode_url(entity, parameters)
        req = self._new_request(url, "PUT")
        if item:
            req.add_data(json.dumps(item))
        else:
            # Fix regarding Nginx not supporting empty requests with no
            # Content-Length
            req.add_header("Content-Length", 0)
        raw = self._urlopen(req)
        if decode:
            return json.load(raw)
        else:
            return raw

    def delete(self, entity, parameters = {}):
        url = self._encode_url(entity, parameters)
        req = self._new_request(url, "DELETE")
        self._urlopen(req)

    def upload_to_exising_file_with_path(self, file_name, path):
        response = fileupload.post_multipart(self._encode_url(path, []), [],
                                             [("file", file_name)],
                                             insecure = self._insecure_upload,
                                             headers = {"Authorization": self._get_basic_authorization_field()})
        return response

    def _encode_url(self, entity, parameters):
        url = self.endpoint + "/" + urllib.quote(entity, "/%")
        if len(parameters) > 0:
            url = url + "?" + urllib.urlencode(parameters)
        return url

    def _headers(self):
        return {
                   "Authorization": self._get_basic_authorization_field(),
                   "Content-Type": "application/json",
                }

    def _get_basic_authorization_field(self):
        s = self.username + ":" + self.password
        return "Basic " + s.encode("base64").rstrip()

    def _urlopen(self, request):
        try:
            return urllib2.urlopen(request)
        except HTTPError as err:
            err_content = err.read()
            try:
                data = json.loads(err_content)
                msg_list = data["error"]
                message = "["
                if len(msg_list) > 0:
                    i = 0
                    while i < len(msg_list) - 1:
                        message += msg_list[i] if msg_list[i] else "None"
                        message += ", "
                        i += 1
                    message += msg_list[len(msg_list) - 1] if msg_list[len(msg_list) - 1] else "None"
                message += "]"
            except Exception:
                message = err_content

            raise ApiException(message, err.code)

    def _new_request(self, url, m):
        return urllibx.RequestWithMethod(url, method = m, headers = self._headers())

    def _new_request_with_data(self, url, m, d):
        return urllibx.RequestWithMethod(url, method = m, headers = self._headers(), data = d)
