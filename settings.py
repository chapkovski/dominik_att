import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings

EMAIL_BACKEND =  'django.core.mail.backends.console.EmailBackend' 
DEFAULT_FROM_EMAIL = 'testing@example.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False 
EMAIL_PORT = 1025
SENTRY_DSN = 'http://406c2b097f3340bca2b45ee7edf1f326:031bfc3a03a34af588ff995aedd0f283@sentry.otree.org/211'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# don't share this with anybody.
# SECRET_KEY = environ.get('SECRET_KEY')

BROWSER_COMMAND = 'firefox'

# To use a database other than sqlite,
# set the DATABASE_URL environment variable.
# Examples:
# postgres://USER:PASSWORD@HOST:PORT/NAME
# mysql://USER:PASSWORD@HOST:PORT/NAME

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [  'localflavor',
                    'otree',
                    'otree_mturk_utils'
                ]

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            oTree auf GitHub
        </a>.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree Webseite
        </a>.
    </li>
</ul>
"""

ROOMS = [
    {
        'name': 'econ101',
        'display_name': 'Econ 101 class',
        'participant_label_file': '_rooms/econ101.txt',
    },
    {
        'name': 'live_demo',
        'display_name': 'Room for live demo (no participant labels)',
    },
    {
         'name': 'session1group1',
         'display_name': 'E-Acc online lab -- session 1, group 1',
         'participant_label_file': '_rooms/ATT2_guestList_session.txt',
    },
    {
        'name': 'session1group2',
        'display_name': 'E-Acc online lab -- session 1, group 2',
        'participant_label_file': '_rooms/ATT2_guestList_session.txt',
    },
    {
        'name': 'session2group1',
        'display_name': 'E-Acc online lab -- session 2, group 1',
        'participant_label_file': '_rooms/ATT2_guestList_session.txt',
    },
    {
        'name': 'session2group2',
        'display_name': 'E-Acc online lab -- session 2, group 2',
        'participant_label_file': '_rooms/ATT2_guestList_session.txt',
    },
]

mturk_hit_settings = {
    'keywords': ['bonus', 'choice', 'study'],
    'title': 'Decision-making study',
    'description': 'Study on group decision-making',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': '3PHD6OHA867ZRXH2RSYNY63A1Z5W9K',
    'grant_qualification_id': '3F9BH0EJUPT46X1CSPR6F0YDNLTKM8', #sandbox
    'qualification_requirements': [
#         {
#             'QualificationTypeId': "00000000000000000071",
#             'Comparator': "EqualTo",
#             'LocaleValues': [{'Country': "US"}]
#         }
#    # ,
        # {
        #     'QualificationTypeId': "3PHD6OHA867ZRXH2RSYNY63A1Z5W9K",
        #     'Comparator': "DoesNotExist",
        # },
        # {
        #     'QualificationTypeId': "3F9BH0EJUPT46X1CSPR6F0YDNLTKM8",
        #     'Comparator': "DoesNotExist",
        # }       
    ]
}

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0,
    'participation_fee': 0,
    'num_bots': 4,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
        {
            'name': 'ATT2_gender',
            'display_name': "Alleviating discrimination experiment with gender IDs",
            'num_demo_participants': 6,
            'app_sequence': [
                # 'consent',
                'ATT2_gender'
            ],
            'use_browser_bots': False,
            'doc': """
            The number of participants needs to be a multiple of (round_number) * 2 
            In this version of the experiment a waiting room after the demographic questions is included.
            """
    }
]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
