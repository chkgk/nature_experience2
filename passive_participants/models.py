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
        with open(C.PAYMENT_FILE, 'r') as f:
            for line in f:
                idn, payment_round, payment = line.strip().split(',')
                payment_data.append((int(idn), int(payment_round), int(payment)))

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


