#!/usr/bin/env python

'Simple replacement for CGI module cgi.FieldStorge() object'

import os
import sys


class FieldStorage:
    'Dummy class to emulate old cgi.FieldStorage'

    def __repr__(self):
        if hasattr(self, "filename"):
            return self.filename
        return f"{self.value}"


def process_request():
    'Process CGI parameters'

    method = os.environ['REQUEST_METHOD']

    if method == "GET":
        return process_get_request()
    if method == "POST":
        return process_post_request()

    raise ValueError("Unsupported REQUEST_METHOD")


def process_get_request():
    '''Process GET request, eg https://host/cgi-bin/foo.cgi?this=that&when=now

    These come in via the QUERY_STRING environment variable.
    The `urllib.parse` routines can be used.
    '''

    from urllib.parse import parse_qsl
    args = parse_qsl(os.environ['QUERY_STRING'], keep_blank_values=True)

    field_storage = {}
    for key, val in args:
        myval = FieldStorage()
        myval.value = val
        field_storage[key] = myval

    return field_storage


def process_post_request():
    '''Process POST request.

    curl -F foo=@bar -F this=that https://host/cgi-bin/boo.cgi

    They come in via stdin as a mutli-part
    message.  Use email `message_from_bytes` to parse into sections.
    File uploads have a filename parameter.  Files u/l can only be
    POST'ed.
    '''

    from email import message_from_bytes

    clen = os.environ["CONTENT_LENGTH"]
    stuff = sys.stdin.buffer.read(int(clen))

    hdr = "Content-Type: "+os.environ["CONTENT_TYPE"]+"\n\n"
    msg = hdr.encode("ascii") + stuff

    em = message_from_bytes(msg)

    field_storage = {}
    for part in em.walk():

        if part.get_content_maintype() == 'multipart':
            # skip over multipart container
            continue

        pname = part.get_param('name', header='content-disposition')

        newpar = FieldStorage()

        fname = part.get_filename()
        if fname:
            newpar.filename = fname
            newpar.value = part.get_payload(decode=1)  # Force binary
        else:
            newpar.value = part.get_payload()

        field_storage[pname] = newpar

    return field_storage


def test_runner():
    'Dummy test program'
    print("Content-type: text/plain\n")
    print(process_request())


if __name__ == '__main__':
    test_runner()
