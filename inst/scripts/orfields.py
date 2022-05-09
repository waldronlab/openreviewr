#!/usr/bin/env python3

from datetime import datetime

class ORFields:

    FIELDS = {
        'Official Venue Name': {
            'required': True,
            'type': str
        },
        'Abbreviated Venue Name': {
            'required': True,
            'type': str
        },
        'Official Website URL': {
            'required': True,
            'type': str
        },
        'Program Chair Emails': {
            'required': True,
            'type': str
        },
        'Contact Email': {
            'required': True,
            'type': str
        },
        'Venue Start Date': {
            'required': True,
            'type': datetime
        },
        'Author And Reviewer Anonymity': {
            'required': True,
            'type': 'single',
            'values': [
                'Double-blind',
                'Single-blind (Reviewers are anonymous)',
                'No anonymity'
            ]
        },
        'Open Reviewing Policy': {
            'required': True,
            'type': 'single',
            'values': [
                'Submissions and reviews should both be private.',
                'Submissions should be public, but reviews should be private.',
                'Submissions and reviews should both be public.'
            ]
        },
        'Signatures': {
            'required': True,
            'type': str
        },
        'Submission Start Date': {
            'required': False,
            'type': datetime,
        },
        'Abstract Registration Deadline': {
            'required': False,
            'type': datetime,
        },
        'Submission Deadline': {
            'required': False,
            'type': datetime,
        },
        'Location': {
            'required': False,
            'type': str
        },
        'Paper Matching': {
            'required': False,
            'type': 'multiple',
            'values': [
                'Reviewer Bid Scores',
                'Reviewer Recommendation Scores',
                'OpenReview Affinity'
            ]
        },
        'Reviewer Identity': {
            'required': False,
            'type': 'multiple',
            'values':[
                'Program Chairs',
                'All Senior Area Chairs',
                'All Area Chairs',
                'Assigned Area Chair',
                'All Reviewers',
                'Assigned Reviewers'
            ]
        }, 
        'Expected Submissions': {
            'required': False,
            'type': int
        },
        'Other Important Information': {
            'required': False,
            'type': str
        },
        'How Did You Hear About Us': {
            'required': False,
            'type': str
        },
        'Area Chairs': {
            'required': False,
            'type': bool,
            'values': {
                'True': 'Yes, our venue has Area Chairs',
                'False': 'No, our venue does not have Area Chairs'
            },
        },
        'Senior Area Chairs': {
            'required': False,
            'type': bool,
            'values': {
                'True': 'Yes, our venue has Senior Area Chairs',
                'False': 'No, our venue does not have Senior Area Chairs'
            }
        },
        'Submission Readers': {
            'required': True,
            'type': 'single',
            'values': [
                'All program committee (all reviewers, all area chairs, all senior area chairs if applicable)',
                'Assigned program committee (assigned reviewers, assigned area chairs, assigned senior area chairs if applicable)',
                'Program chairs and paper authors only',
                'Everyone (submissions are public)'
            ]
        },
        'Submissions Visibility': {
            'required': False,
            'type': bool,
            'values': {
                'True': 'Yes, submissions should be immediately revealed to the public.',
                'False': 'No, wait until the submission deadline has passed to make them public.'
            }
        },
        'Withdrawn Submissions Visibility': {
            'required': False,
            'type': bool,
            'values': {
                'True': 'Yes, withdrawn submissions should be made public.',
                'False': 'No, withdrawn submissions should not be made public.'
            }
        },
        'Withdrawn Submissions Author Anonymity': {
            'required': False,
            'type': bool,
            'values': {
                'True': 'Yes, author identities of withdrawn submissions should be revealed.',
                'False': 'No, author identities of withdrawn submissions should not be revealed.'
            }
        },
        'Email Pcs For Withdrawn Submissions': {
            'required': False,
            'type': bool,
            'values': {
                'True': 'Yes, email PCs.',
                'False': 'No, do not email PCs.'
            }
        },
        'Desk Rejected Submissions Visibility': {
            'required': False,
            'type': bool,
            'values': {
                'True': 'Yes, desk rejected submissions should be made public.',
                'False': 'No, desk rejected submissions should not be made public.'
            }
        },
        'Desk Rejected Submissions Author Anonymity': {
            'required': False,
            'type': bool,
            'values': {
                'True': 'Yes, author identities of desk rejected submissions should be revealed.',
                'False': 'No, author identities of desk rejected submissions should not be revealed.'
            }
        },
        'Email Pcs For New Submissions': {
            'required': False,
            'type': bool,
            'values': {
                'True': 'Yes, email PCs for every new submission.',
                'False': 'No, do not email PCs.'
            }
        }
    }

    def required(self) -> list:
        return [f for f, a in self.FIELDS.items() if a['required']]

    def optional(self) -> list:
        return [f for f, a in self.FIELDS.items() if not a['required']]

    def datetime(self) -> list:
        return [f for f, a in self.FIELDS.items() if a['type'] == datetime]

    def single(self) -> list:
        return [f for f, a in self.FIELDS.items() if a['type'] == 'single']

    def multiple(self) -> list:
        return [f for f, a in self.FIELDS.items() if a['type'] == 'multiple']

    def get_value(self, field: str, option: str) -> str:
        """Return value for field and option combination

        Parameters
        ----------
        field : str
            Field name in OpenReview

        option : str
            A value corresponding to a valid response in OpenReview

        Returns
        -------
        str
            The corresponding respose in OpenReview

        Raises
        ------
        KeyError
            if option doesn't exist
        """

        try:
            return self.FIELDS[field]['values'][option]
        except KeyError as err:
            print(f'{option} is not a valid option for {field}.')
            raise err

    def are_valid(self, field: str, options : str) -> bool:
        """Return True if field and options combinations are valid 

        Parameters
        ----------
        field : str
            Field name in OpenReview

        options : str
            Value(s) corresponding to OpenReview response

        Returns
        -------
        bool
            True if the options are valid OpenReview responses
        """

        if self.FIELDS[field]['type'] == 'multiple':
            options = [option.strip() for option in options.split(',')]
        else:
            options = [options]
        return set(options).issubset(set(self.FIELDS[field]['values']))
