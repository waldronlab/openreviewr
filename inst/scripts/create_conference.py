#!/usr/bin/env python3

import argparse
import configparser
import datetime
from email.utils import parseaddr
import openreview
import os


class ConferenceCreator:

    WEBSITE = 'Microbiome-VIF.org'

    @staticmethod
    def _valid_date(year: str, month: str, day: str) -> datetime.datetime:
        """Return a valid datetime

        Parameters
        ----------
        year : str
            Four character year
        month : str
            Two character month
        day : str
            Two character day

        Returns
        -------
        datetime.datetime
            A valid date

        Raises
        -------
        ValueError
            If date is invalid
        """

        try:
            return datetime.datetime(year = int(year),
                                     month = int(month),
                                     day = int(day))
        except ValueError as err:
            print(f'{year}/{month}/{day} is not a valid date.')

    @staticmethod
    def _read(path: str) -> dict:
        """Read the configuration file

        Parameters
        ----------
        path : str
            Path to the configuration file 

        Returns
        -------
        dict 
            A dict of configuration valid options and values
        """

        cp = configparser.ConfigParser()
        cp.read(path)

        for field in ['Title', 'Subtitle', 'Location']:
            if type(cp['CONFERENCE'][field]) != str and \
                cp['CONFERENCE'][field] == '':
                print(f"{cp['CONFERENCE'][field]} must be a non-empty string.")
                return {}

        try:
            int(cp['CONFERENCE']['Number'])
        except ValueError as err:
            print(f"{cp['CONFERENCE']['Number']} is not a valid Number")
            return {}

        dates = {'event': (['CONFERENCE']['Year'],
                            ['CONFERENCE']['Month'],
                            ['CONFERENCE']['Day']),
                 'deadline': (['CONFERENCE']['DeadlineYear'],
                              ['CONFERENCE']['DeadlineMonth'],
                              ['CONFERENCE']['DeadlineDay'])
        }

        valid_dates = {'event': '', 'deadline': ''}
        for name, (year, month, day) in dates:
            try:
                valid_dates[name] = self._valid_date(year, month, day)
            except ValueError as err:
                print('{name} date is not valid.')
                return {}

        if valid_dates['event'] <= datetime.datetime.now():
            print(f'The event date must be a valid future date.')
            return {}

        if valid_dates['event'] < valid_dates['deadline']:
            print(f'The deadline date must be valid future date.')
            return {}

        _, email = parseaddr(cp['CONFERENCE']['Contact'])
        if not email:
            print(f'Contact must be a valid email.')
            return {}

        for email in cp['GROUP']['Members'].split():
            _, e = parseaddr(email)
            if not e:
                print(f'Members must be valid emails separated by spaces.')
                return {}

        if not os.path.isfile(cp['TEMPLATE']['Path']):
            print(f"{cp['TEMPLATE']['Path']} not found.")
            return {}

        return {
            'title': cp['CONFERENCE']['Title'],
            'subtitle': cp['CONFERENCE']['Subtitle'],
            'location': cp['CONFERENCE']['Location'],
            'number': int(cp['CONFERENCE']['Number']),
            'year': int(cp['CONFERENCE']['Year']),
            'month': int(cp['CONFERENCE']['Month']),
            'day': int(cp['CONFERENCE']['Day']),
            'contact': cp['CONFERENCE']['Contact'],
            'readers': cp['GROUP']['Readers'],
            'members': cp['GROUP']['Members'].split(),
            'path': cp['TEMPLATE']['Path']
        }

    def __init__(self, user: str, password: str, path: str) -> None:
        """Create a ConferenceCreator object

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
        try:
            self.client = openreview.Client(url, user, password)
        except openreview.OpenReviewException as ore:
            print(f"ore['error']: ore['message']")
        if not os.path.isfile(path):
            print(f'{path} not found.')
        else:
            self.config = self._read(path)

    def valid(self) -> bool:
        """Return True if config and client are set"""

        return self.config != {} && self.client

    def get_new_group_name(self) -> str:
        """Return the new group name"""

        return f"{self.WEBSITE}/n{self.config['number']}" 

    def create_group(self) -> openreview.Group:
        """Create a group and its subgroups"""

        new_group = self.get_new_group_name()
        groups = openreview.tools.build_groups(new_group)
        for group in groups:
            if group.id == new_group:
                group.members = ['~' + m for m in self.config['members']]
                group.web = self.config['path']
            self.client.post_group(group, overwrite = False)
        return groups[-1]

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
    cc = ConferenceCreator(args.email.pop(),
                           args.password.pop(),
                           args.config.pop()) 

    if cc.valid():
        new_group = cc.create_group()
        print(f'{new_group} created.')
    else:
        print(f'Failed group creation. Check the template files are valid.')
