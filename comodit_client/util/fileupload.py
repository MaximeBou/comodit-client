import mimetypes, pycurl

class PyCurlCallBack(object):
    def __init__(self):
        self.response = ''

    def response_callback(self, response):
        self.response += response

def post_multipart(url, fields, files, insecure = False, headers = {}):
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.URL, str(url))

    if insecure:
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)

    # Build header
    curl_headers = []
    for key in headers:
        curl_headers.append(key + ":" + headers[key])
    c.setopt(c.HTTPHEADER, curl_headers)

    # Add data
    for (key, value) in fields:
        c.setopt(c.HTTPPOST, [(key, value)])

    # Add files
    curl_files = []
    for (key, filename) in files:
        curl_files.append((key, (c.FORM_FILE, str(filename))))
    c.setopt(c.HTTPPOST, curl_files)

    # Set callback
    callback = PyCurlCallBack()
    c.setopt(c.WRITEFUNCTION, callback.response_callback)

    c.perform()
    c.close()

    return callback.response

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
