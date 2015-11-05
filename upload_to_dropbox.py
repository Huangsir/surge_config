#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib3
urllib3.disable_warnings()

import json
import sys
from os import path
from dropbox import client


def do_login(app_key, app_secret, code):
    flow = client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    flow.start()
    try:
        token, _ = flow.finish(code.strip())
        return token
    except Exception as e:
        print "Error login: ", e


def make_token(flush=False):
    token = ""
    data = {}
    with open("dropbox.txt", "r") as fp:
        data = json.loads(fp.read())
        token = data.get("token", "")

    if flush or not token:
        token = do_login(data.get("app_key"), data.get("app_secret"), data.get("code"))
        data["token"] = token
        with open("dropbox.txt", "w") as fp:
            fp.write(json.dumps(data))

    return token


def make_client():
    token = make_token()
    for _ in xrange(3):
        try:
            api_client = client.DropboxClient(token)
            return api_client
        except Exception as e:
            token = make_token(True)
            print "Error: ", e


def main():
    filepath = sys.argv[1]
    filename = path.basename(filepath)

    cli = make_client()
    cli.put_file("./%s" % filename, filepath, True)

if __name__ == "__main__":
    main()
