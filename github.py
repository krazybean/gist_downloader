import json
import config
import requests
import warnings
from pprint import pprint
from base64 import encodestring as base64
from requests.packages.urllib3 import exceptions
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

conf = config.Configs()


class Github:
    """ Github handler for this project """

    def __init__(self):
        """ Setup for variables """
        self.github_host = conf.github()['host']
        self.api = self.github_host
        if 'github.com' not in self.github_host:
            self.api = "https://{0}/api/v3".format(self.github_host)

    def repo_details(self, repo):
        """ returns github details for repo in config """
        gitdetails = conf.get_repo(repo)
        git_user = gitdetails['username']
        git_token = gitdetails['token']
        return git_user, git_token

    def auth(self):
        """ grabs the creds for a specific repo """
        user_creds = conf.get_creds()
        username = user_creds['username']
        token = user_creds['token']
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'token {0}'.format(token)}
        return headers

    def list_repos(self):
        """ return a list of all repos in config """
        repolist = []
        for repo in conf.get_repo_list():
            repolist.append(repo)
        return repolist

    def list_gists(self, username):
        """ returns a list of gists under specified user """
        # GET /users/:username/gists
        headers = self.auth()
        gist_uri = "/users/{0}/gists".format(username)
        url = "{0}{1}".format(self.api, gist_uri)
        req = requests.get(url, headers=headers, verify=False)
        return req.json()

    def get_gist(self, gist_url):
        """ returns details of specific gist """
        headers = self.auth()
        req = requests.get(gist_url, headers=headers, verify=False)
        return req.json()

    def format_gist(self, gist):
        """ pull out elements needed for post """
        ignore = ['filename', 'language', 'raw_url', 'size',
                  'truncated', 'type']
        new_files = {'files': {}}
        new_files['description'] = gist['description']
        new_files['public'] = gist['public']
        new_files['files'] = {}
        files = gist['files']
        for file_name in files:
            new_files['files'][file_name] = {}
            new_files['files'][file_name]['content'] =\
                files[file_name]['content']
        return new_files

    def restructure(self):
        username = conf.git_user()['user']
        list_of_gists = self.list_gists(username)
        count = 0
        for gist in list_of_gists:
            gist_url = gist['url']
            output = self.get_gist(gist_url)
            files = self.format_gist(output)
            count += 1


if __name__ == '__main__':
    g = Github()
    print g.restructure()
