#!/usr/bin/env python

import os
from ConfigParser import SafeConfigParser, NoOptionError


class Configs:
    """ Grab data from configs """

    def __init__(self):
        """ Setup """
        CONFIGFILE = 'settings.conf'
        self.settings = SafeConfigParser()
        curdir = os.path.dirname(os.path.realpath(__file__))
        configfile = "{0}/{1}".format(curdir, CONFIGFILE)
        self.settings.read(configfile)

    def get_creds(self):
        """ returns a dict of username, token """
        username = self.settings.options('username')[0]
        token = self.settings.get('username', username)
        return {'username': username, 'token': token}

    def github(self):
        """ Kinda lame that this only returns github host """
        return {'host': self.settings.get('github', 'host')}

    def git_user(self):
        """ returns just the github user in config"""
        # this is added because the auth user may not be the same as git user
        return {'user': self.settings.get('github', 'user')}

if __name__ == '__main__':
    c = Configs()
    print c.get_creds()
    print c.github()['host']
