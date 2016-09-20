#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import config
from github import Github

DOWNLOAD_PATH = "{0}/.gists".format(os.path.expanduser('~'))

conf = config.Configs()

g = Github()


def download(directory):
    count = 0
    if not os.path.isdir(directory):
        print("Creating directory {0}".format(directory))
        os.mkdir(directory, 0755)
    username = conf.git_user()['user']
    print("Saving {0} gists to {1}".format(username, directory))
    list_of_gists = g.list_gists(username)
    for count, gist in enumerate(list_of_gists):
        filename = gist['id']
        filepath = "{0}/{1}.txt".format(directory, filename)
        if not os.path.isfile(filepath):
            gist_url = gist['url']
            output = g.get_gist(gist_url)
            files = g.format_gist(output)
            f = open(filepath, 'w+')
            f.write(str("Filename: {0}\n".format(filename)))
            f.write(str("Public: {0}\n".format(files['public'])))
            f.write(str("Description: {0}\n".format(files['description'])))
            for item in files:
                if item == 'files':
                    for row, filei in enumerate(files['files'].keys()):
                        f.write("\n===== {0} Content =====\n".format(filei))
                        raw = files['files'][filei]['content']
                        f.write(raw.encode('utf-8'))
                        print("--[File {0} = {1}".format(row, filei))
            f.close()
            print("File {0} created.".format(filename))
        else:
            print("File {0} already exists, skipping...".format(filename))
        if count > 9:
            break
    print(count)

download(DOWNLOAD_PATH)
