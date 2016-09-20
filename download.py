#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import config
from github import Github
import requests

DOWNLOAD_PATH = "{0}/.gists".format(os.path.expanduser('~'))

conf = config.Configs()

g = Github()


def download(directory):
    headers = {'Link': ''}
    page = 1
    if not os.path.isdir(directory):
        print("Creating directory {0}".format(directory))
        os.mkdir(directory, 0755)
    username = conf.git_user()['user']
    print("Saving {0} gists to {1}".format(username, directory))
    while True:
        if 'rel="next"' not in headers['Link'] and headers['Link'] != '':
            break
        print("Iterating to page {0}".format(page))
        try:
            headers, list_of_gists = g.list_gists(username, page=page)
        except requests.exceptions.ConnectTimeout:
            print("Timeout connecting to github")
            break
        for count, gist in enumerate(list_of_gists):
            count += 1
            filename = gist['id']
            filepath = "{0}/{1}.txt".format(directory, filename)
            if not os.path.isfile(filepath):
                print("Creating File {0}.".format(filename))
                gist_url = gist['url']
                output = g.get_gist(gist_url)
                files = g.format_gist(output)
                f = open(filepath, 'w+')
                f.write(str("Filename: {0}\n".format(filename)))
                f.write(str("Public: {0}\n".format(files['public'])))
                description = files['description']
                f.write(str("Description: {0}\n".format(description)))
                for item in files:
                    if item == 'files':
                        for row, filei in enumerate(files['files'].keys()):
                            row += 1
                            print("--[File {0} = {1}]--".format(row, filei))
                            f.write("\n==== {0} Content ====\n".format(filei))
                            raw = files['files'][filei]['content']
                            f.write(raw.encode('utf-8'))
                f.close()
            else:
                pass
                # print("File {0} exists, skipping...".format(filename))
        page += 1
        print(count)

download(DOWNLOAD_PATH)
