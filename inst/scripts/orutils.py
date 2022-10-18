#!/usr/bin/env python3

import configparser
from datetime import datetime
from email.utils import parseaddr
import json
import os

from orfields import ORFields

class ORUtils:

    @staticmethod
    def is_valid(date_or_datetime: str, time: bool) -> datetime:
        """Return a valid datetime

        Parameters
        ----------
        date_or_datetime : str
            YYYY/MM/DD or YYYY/MM/DD HH:MM

        time : bool
            if True, date_or_datetime is a datetime

        Returns
        -------
        datetime
            A valid date or datetime

        Raises
        -------
        ValueError
            If date is invalid
        """

        format = '%Y/%m/%d %H:%M' if time else '%Y/%m/%d'
        try:
            return datetime.strptime(date_or_datetime, format)
        except ValueError as err:
            message = 'datetime' if time else 'date'
            print(f'{date_or_datetime} is not a valid {message}.')

    @staticmethod
    def read(path: str) -> dict:
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

        response = {}
        orf = ORFields()

        cp = configparser.ConfigParser()
        cp.read(path)

        required_fields = orf.required()
        optional_fields = [f for f in orf.optional() if cp['OPTIONAL'][f] != '']
        multiple_fields = orf.multiple()
        single_and_multiple_fields = orf.single() + multiple_fields

        for field in required_fields:
            if cp['REQUIRED'][field] == '':
                print(f'{field} is required.')
                return {}

        if cp['OPTIONAL']['Expected Submissions']:
            try:
                int(cp['OPTIONAL']['Expected Submissions'])
            except ValueError as err:
                print(f'Expected Submissions must be a number.')
                return {}

        for field in orf.datetime():
            section = 'REQUIRED' if field in required_fields else 'OPTIONAL'
            if cp[section][field]:
                try:
                    is_datetime = True if field != 'Venue Start Date' else False
                    ORUtils.is_valid(cp[section][field], is_datetime)
                except ValueError as err:
                    print(f'{field} is not valid: ')
                    print(err)
                    return {}

        email_dict = {
            'Contact Email': [cp['REQUIRED']['Contact Email']],
            'Program Chair Emails':
                 ORUtils.to_list(cp['REQUIRED']['Program Chair Emails']),
            'Signatures': ORUtils.to_list(cp['REQUIRED']['Signatures'])
        }

        for field, emails in email_dict.items():
            if len(emails) > 1 and not ORUtils.valid_emails(emails):
                print(f'{field} must have valid emails separated by commas')
                return {}
            elif len(emails) == 1 and not ORUtils.valid_email(emails):
                print(f'{field} must be a valid email')
                return {}

        boolean_fields = \
            [f for f in optional_fields if orf.FIELDS[f]['type'] == bool]

        for field in boolean_fields:
            if orf.FIELDS[field]['type'] == bool and \
                cp['OPTIONAL'][field] not in orf.FIELDS[field]['values'].keys():
                print(f'{field} must be True or False.')
                return {}
            else:
                response[field] = orf.get_value(field, cp['OPTIONAL'][field])

        for field in single_and_multiple_fields:
            section = 'REQUIRED' if field in required_fields else 'OPTIONAL'
            if cp[section][field] != '' and \
                not orf.are_valid(field, cp[section][field]):
                print(f'{cp[section][field]} is not valid for {field}.')
                return {}
            elif field in multiple_fields:
                response[field] = ORUtils.to_list(cp[section][field])

        # The following keys match the representation in the OpenReview API
        # Area Chair Identity and Senior Area Chair Identity are also hardcoded
        config = {
            'title': cp['REQUIRED']['Official Venue Name'], 
            'Official Venue Name': cp['REQUIRED']['Official Venue Name'],
            'Abbreviated Venue Name': cp['REQUIRED']['Abbreviated Venue Name'],
            'Official Website URL': cp['REQUIRED']['Official Website URL'],
            'program_chair_emails': email_dict['Program Chair Emails'],
            'contact_email': cp['REQUIRED']['Contact Email'],
            'Area Chairs (Metareviewers)': response['Area Chairs'],
            'senior_area_chairs': response['Senior Area Chairs'],
            'Submission Start Date': cp['OPTIONAL']['Submission Start Date'],
            'abstract_registration_deadline':
                 cp['OPTIONAL']['Abstract Registration Deadline'],
            'Submission Deadline': cp['OPTIONAL']['Submission Deadline'],
            'Venue Start Date': cp['REQUIRED']['Venue Start Date'],
            'Location': cp['OPTIONAL']['Location'],
            'Paper Matching': response['Paper Matching'],
            'Author and Reviewer Anonymity': cp['REQUIRED']['Author And Reviewer Anonymity'],
            'reviewer_identity': response['Reviewer Identity'],
            'Open Reviewing Policy': cp['REQUIRED']['Open Reviewing Policy'],
            'submission_readers': cp['REQUIRED']['Submission Readers'],
            'submissions_visibility': response['Submissions Visibility'],
            'withdrawn_submissions_visibility':
                 response['Withdrawn Submissions Visibility'],
            'withdrawn_submissions_author_anonymity':
                 response['Withdrawn Submissions Author Anonymity'],
            'email_pcs_for_withdrawn_submissions':
                 response['Email Pcs For Withdrawn Submissions'],
            'desk_rejected_submissions_visibility':
                 response['Desk Rejected Submissions Visibility'],
            'desk_rejected_submissions_author_anonymity':
                 response['Desk Rejected Submissions Author Anonymity'],
            'Expected Submissions': cp['OPTIONAL']['Expected Submissions'],
            'email_pcs_for_new_submissions':
                 response['Email Pcs For New Submissions'],
            'Other Important Information':
                 cp['OPTIONAL']['Other Important Information'],
            'How did you hear about us?':
                 cp['OPTIONAL']['How Did You Hear About Us'],
            'area_chair_identity': ['Program Chairs'],
            'senior_area_chair_identity': ['Program Chairs'],
            'submission_name': 'Submission',
            'venue_id': '',
            'signatures': email_dict['Signatures']
            }
        return {k:v for k, v in config.items() if v != ''}

    @staticmethod
    def to_list(values: str) -> list:
        """Return values as list

        Parameters
        ----------
        values: str

        Returns
        -------
        list
        """

        return [value.strip() for value in values.split(',')]

    @staticmethod
    def valid_email(an_email: str) -> bool:
        """Return True if email is valid

        Parameters
        ----------
        an_email : str

        Returns
        -------
        bool
        """

        _, email = parseaddr(an_email)
        return '@' in email

    @staticmethod
    def valid_emails(emails: list) -> bool:
        """Return True if all emails are valid

        Parameters
        ----------
        emails : list

        Returns
        -------
        bool
        """

        valid = True
        for email in emails:
            valid &= ORUtils.valid_email(email)
        return valid

    @staticmethod
    def venue_id(abbreviated_venue_name: str, venue_start_date: str) -> str:
        """Return the venue id

        Parameters
        ----------
        abbreviated_venue_name : str

        venue_start_date : str

        Returns
        -------
        str
        """

        venue, _, number = abbreviated_venue_name.split(' ')
        number = number.strip(')')
        year = venue_start_date.split('/')[0]
        return f'{venue}.org/{year}/Forum/Round{number}'
