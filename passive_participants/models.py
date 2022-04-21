from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as cu,
    currency_range,
)
import itertools
import csv


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'passive_participants'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    BALL_GREEN_PROBABILITY = 0.8
    ACTION_B_PROBABILITY = 0.4

    PAYMENT_FILE = 'payments.csv'


class Subsession(BaseSubsession):
    def creating_session(self):
        payment_data = []
        with open(C.PAYMENT_FILE, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # print(row)
                # idn, payment_round, payment, s, p = line.strip().split(',')
                payment_data.append((int(row['idn']), int(row['payment_round']), int(row['payment'])))

        self.session.vars['payments'] = itertools.cycle(payment_data)  # this should never reach the end, but we cycle just in case


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payment_id = models.IntegerField()
    payment_round = models.IntegerField()

    def get_payment_data(self):
        idn, payment_round, payment = next(self.session.vars['payments'])
        self.payment_id = idn
        self.payment_round = payment_round
        self.payoff = payment

        # survey

    age = models.IntegerField(
        verbose_name='What is your age?',
        min=16, max=99,
        doc="Participant's age"
    )

    gender = models.StringField(
        choices=['Male', 'Female', 'Other', 'I prefer not to tell'],
        verbose_name='What is your gender?',
        widget=widgets.RadioSelect,
        doc="Participant's gender"
    )
