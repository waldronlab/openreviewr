#!/usr/bin/env python3

import argparse
import configparser
from datetime import datetime
import json
import openreview
import os

from orfields import ORFields
from orutils import ORUtils


class PostRequestFormNote:

    def __init__(self, user: str, password: str, path: str) -> None:
        """Create a PostRequestFormNote object with updated Signatures

        Parameters
        ----------
        user : str
            User login name
        password : str
            User password
        path : str
            Path to the configuration *.ini file
        """

        url = 'https://api.openreview.net'
        self.client = False
        self.config = {}
        self.signatures = []
        try:
            self.client = openreview.Client(url, user, password)
        except openreview.OpenReviewException as ore:
            print(f"ore['error']: ore['message']")
        if not os.path.isfile(path):
            print(f'{path} not found.')
        else:
            self.config = ORUtils.read(path)
            for signature in self.config['signatures']:
                profile = self.client.get_profile(signature)
                self.signatures.append(profile.id)
            del self.config['signatures']

    def create_note(self) -> openreview.Note:
        """Create an openreview.Note"""

        invitation = 'OpenReview.net/Support/-/Request_Form'
        readers = ['OpenReview.net/Support'] + self.signatures + \
            self.config['program_chair_emails']
        return openreview.Note(invitation = invitation,
                               readers = readers,
                               writers = [],
                               signatures = self.signatures,
                               content = self.config)

    def post_request_form_note(self) -> bool:
        """Post a request form note to OpenReview"""

        return self.client.post_note(self.create_note())

    def valid(self) -> bool:
        """Return True if config and client are set"""

        return self.config != {} and self.client

if __name__ == '__main__':
    parser_description = 'Waldron Lab OpenReview Conference Creator'
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument('email', nargs='+', type=str, default='',
                        help='User email in OpenReview.net')
    parser.add_argument('password', nargs='+', type=str, default='',
                        help='User password in OpenReview.net')
    parser.add_argument('config', nargs=1, type=str, default='',
                        help='Path to the configuration .ini file.')
    args = parser.parse_args()
    prfn = PostRequestFormNote(args.email.pop(),
                               args.password.pop(),
                               args.config.pop()) 

    if prfn.valid():
        print(prfn.post_request_form_note())
        #print(prfn.config)
    else:
        print('Invalid note. Check that your template files are valid.')
