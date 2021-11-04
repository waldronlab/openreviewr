#!/usr/bin/python

## Install using:
# pip install openreview-py


import os
import openreview

## See https://openreview-py.readthedocs.io/en/latest/ for documentation
## https://openreview-py.readthedocs.io/en/latest/workshop.html for "Creating a Conference"

## Either replace os.environ.get('OPENREVIEW_USERNAME') and os.environ.get('OPENREVIEW_PASSWORD') with your openreview username and password, or place lines like this
## in your .bash_profile or entered on the command line (without the #):
# export OPENREVIEW_USERNAME="YourOpenreviewEmailHere"
# export OPENREVIEW_PASSWORD="YourPasswordHere"

client = openreview.Client(baseurl='https://api.openreview.net',
                           username=os.environ.get('OPENREVIEW_USERNAME'),
                           password=os.environ.get('OPENREVIEW_PASSWORD'))


client.post_group(openreview.Group(id = 'Microbiome-VIF.org/n5',
                                   readers = ['everyone'],
                                   writers = ['OpenReview.net'],
                                   signatories = ['Microbiome-VIF.org/n5'],
                                   signatures = ['OpenReview.net']))


client.post_group(openreview.Group(id = 'Microbiome-VIF.org/n5',
                                   readers = ['everyone'],
                                   writers = ['Microbiome-VIF.org/n5'],
                                   signatories = ['Microbiome-VIF.org/n5'],
                                   signatures = ['Microbiome-VIF.org/n5'],
                                   members = ['~serena.manara@unitn.it','~levi.waldron@sph.cuny.edu','~jennifer.wokaty@sph.cuny.edu','~samuel.gamboa.tuz@gmail.com'],
                                   web = '/home/lwaldron/code/MVIF/conference_template.js'))
