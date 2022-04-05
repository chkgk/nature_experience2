from os import environ

SESSION_CONFIGS = [
    {
        'name': 'v3_bot_ra',
        'display_name': "Bot - Active",
        'num_demo_participants': 2,
        'app_sequence': ['two_natural'],
        'treatment': 'RA'
    },
    {
        'name': 'v3_bot_payments',
        'display_name': "Bot - Passive",
        'num_demo_participants': 2,
        'app_sequence': ['passive_participants'],
    }
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.50,
    'doc': "",
    'mturk_hit_settings': dict(
        keywords='bonus, study, research, decision making',
        title='Short Research Study (ca. 7min)',
        description='Participate in a game and a short survey.',
        frame_height=700,
        template='two_natural/mturk_template.html',
        minutes_allotted_per_assignment=15,
        expiration_hours=3,
        qualification_requirements=[
            {
                'QualificationTypeId': '00000000000000000071',
                'Comparator': 'EqualTo',
                'LocaleValues': [{'Country': "US"}]
            },
            # NoA 2021
            {
                'QualificationTypeId': '3KOC1385AO2HOJ2HF551PYPM8EABYP',
                'Comparator': 'DoesNotExist'
            },
            {
                'QualificationTypeId': '3KOC1385AO2HOJ2HF551PYPM8FRBY8',
                'Comparator': 'DoesNotExist'
            },
        ],
        grant_qualification_id='3KOC1385AO2HOJ2HF551PYPM8FRBY8',  # to prevent retakes
    )
}

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9378732542548'
