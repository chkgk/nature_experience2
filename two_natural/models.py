from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as cu, currency_range
)

import random

author = 'Christian König-Kersting'

doc = """
V3 of Nature of Experience Project, Bot Treatment
"""


class C(BaseConstants):
    NAME_IN_URL = 'two_natural'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    COMPREHENSION_SOLUTIONS = {
        'c1_coplayer': 2,
        'c2_partner': 1,
        'c3_probabilities': 1,
        'c4_decision_importance': 2,
        'c5_payoff_ab_red': 1,
        'c6_payoff_ab_green': 2,
        'c7_payoff_bb_green': 1,
        'c8_payoff_ba_green': 3
    }

    BALL_GREEN_PROBABILITY = 0.8
    ACTION_B_PROBABILITY = 0.4

    # note: False = red, True = green
    PAYOFF_MATRIX = {
        False:
            {
                False: 1,
                True: 1
            },
        True:
            {
                False: 3,
                True: 0
            }
    }

    MIN_WAIT = 5  # change back to 5


class Subsession(BaseSubsession):
    def creating_session(self):
        config_treatment = self.session.config.get('treatment')

        for player in self.get_players():
            if config_treatment not in ['AA', 'RA']:
                treatment = random.choice(['AA', 'RA'])
            else:
                treatment = config_treatment

            player.aa_treatment = treatment == 'AA'
            player.ra_treatment = treatment == 'RA'
            player.payment_room_1 = random.choice([True, False])

            player.participant.vars["aa_treatment"] = player.aa_treatment
            player.participant.vars["ra_treatment"] = player.ra_treatment
            player.participant.vars["payment_room_1"] = player.payment_room_1
            player.participant.vars["bot_treatment"] = player.bot_treatment


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    aa_treatment = models.BooleanField(initial=False, doc="True (1) if AA treatment, else False (0)")
    ra_treatment = models.BooleanField(initial=False, doc="True (1) if RA treatment, else False (0)")
    bot_treatment = models.BooleanField(initial=True, doc="True (1) if bot treatment, else False (0)")

    payment_room_1 = models.BooleanField(
        doc="True (1) if room 1 is selected for payment, False (0) if room 2 is selected.")

    c1_coplayer = models.IntegerField(
        choices=[[1, 'other human participants.'],
                 [2, 'computers.']],
        verbose_name='1. Which of the following is correct? My co-players are always',
        doc="Answer to comprehension question 1 (co-player)",
        widget=widgets.RadioSelect)

    c2_partner = models.IntegerField(
        choices=[[1, 'another human.'],
                 [2, 'a computer.']],
        verbose_name='2. Which of the following is correct? The passive participant receiving the payment is',
        doc="Answer to comprehension question 2 (passive player)",
        widget=widgets.RadioSelect)

    c3_probabilities = models.IntegerField(
        choices=[[1, 'choose A more often than B.'],
                 [2, 'choose B more often than A.'],
                 [3, 'choose A and B equally often.']],
        doc="Answer to comprehension question 3 (probabilities of A and B)",
        verbose_name='3. Which of the following is correct? On average, co-players',
        widget=widgets.RadioSelect)

    c4_decision_importance = models.IntegerField(
        choices=[[1, 'The outcome of round 1 is less important than the outcome of round 2.'],
                 [2, 'The outcomes of both rounds are equally important.'],
                 [3, 'The outcome of round 2 is less important than the outcome of round 1.']],
        verbose_name='4. Remember that only one of the two rounds counts for your payment, with equal chance. What does this mean?',
        doc="Answer to comprehension question 4 (decision importance of the two rounds)",
        widget=widgets.RadioSelect)

    c5_payoff_ab_red = models.IntegerField(
        choices=[[1, 'US$ 0'],
                 [2, 'US$ 1'],
                 [3, 'US$ 3']],
        verbose_name="5. What is your payout if your action is A, your co-player’s action is B, and the ball is red?",
        doc="Answer to comprehension question 5 (payoff AB, red)",
        widget=widgets.RadioSelect)

    c6_payoff_ab_green = models.IntegerField(
        choices=[[1, 'US $ 0'],
                 [2, 'US $ 1'],
                 [3, 'US $ 3']],
        verbose_name="6. What is your payout if your action is A, your co-player’s action is B, and the ball is green?",
        doc="Answer to comprehension question 6 (payoff AB, green)",
        widget=widgets.RadioSelect)

    c7_payoff_bb_green = models.IntegerField(
        choices=[[1, 'US $ 0'],
                 [2, 'US $ 1'],
                 [3, 'US $ 3']],
        verbose_name="7. What is your payout if your action is B, your co-player’s action is B, and the ball is green?",
        doc="Answer to comprehension question 7 (payoff BB, green)",
        widget=widgets.RadioSelect)

    c8_payoff_ba_green = models.IntegerField(
        choices=[[1, 'US $ 0'],
                 [2, 'US $ 1'],
                 [3, 'US $ 3']],
        verbose_name="8. What is your payout if your action is B, your co-player’s action is A, and the ball is green?",
        doc="Answer to comprehension question 8 (payoff BA, green)",
        widget=widgets.RadioSelect)

    prefers_b = models.BooleanField(
        choices=[(False, 'Action A'), (True, 'Action B')],
        verbose_name="A final question, for which there is no right or wrong answer: Which action would you choose?",
        blank=True,
        doc="Preferred action, AA treatment only.",
        widget=widgets.RadioSelect)

    action1_b = models.BooleanField(
        choices=[(False, "A"), (True, "B")],
        widget=widgets.RadioSelect(),
        verbose_name="Which action do you choose?",
        doc="Round 1, True (1) if participant chose B, else False (0).")

    # beliefs
    green_red_r1 = models.IntegerField(min=0, max=100, doc="Round 1, Belief about ball being red (0) or green (100).")
    a_or_b_r1 = models.IntegerField(min=0, max=100, doc="Round 1, Belief about others' action being A (0) or B (100)")

    def set_participant_var(self):
        self.participant.vars["action1_b"] = self.action1_b

    action2_b = models.BooleanField(
        choices=[(False, "A"), (True, "B")],
        widget=widgets.RadioSelect(),
        verbose_name="Which action do you choose?",
        doc="Round 2, True (1) if participant chose B, else False (0).")

    switcher = models.BooleanField(
        doc="True (1) if participant switched actions (A/B) between rounds.")

    # beliefs
    green_red_r2 = models.IntegerField(min=0, max=100, doc="Round 1, Belief about ball being red (0) or green (100).")
    a_or_b_r2 = models.IntegerField(min=0, max=100, doc="Round 1, Belief about others' action being A (0) or B (100)")

    # motivations for action choice in secound round
    motivation = models.IntegerField(min=1, max=6,
                                     doc="Motivation selected for switching, respectively sticking to the same action.")
    motivation_other = models.CharField(blank=True, doc="Free text input for other motivations if motivation == 6")

    def determine_switch(self):
        self.switcher = self.action1_b != self.action2_b
        self.participant.vars["action2_b"] = self.action2_b
        self.participant.vars["switcher"] = self.switcher

    ball_green_r1 = models.BooleanField(doc="True (1) if color of ball drawn is green in round 1, else False (0).")
    ball_green_r2 = models.BooleanField(doc="True (1) if color of ball drawn is green in round 2, else False (0).")

    def draw_ball_r1(self):
        self.ball_green_r1 = random.random() < C.BALL_GREEN_PROBABILITY

    def draw_action_r1(self):
        self.other_b_r1 = random.random() < C.ACTION_B_PROBABILITY

    other_b_r1 = models.BooleanField(doc="True (1) if co-player played B in round 1, else False (0).")
    room_payoff_r1 = models.CurrencyField(doc="Payoff for room 1, if selected for payment.")

    def calculate_payoff_r1(self):
        if self.other_b_r1 is not None:
            if self.ball_green_r1:
                self.room_payoff_r1 = cu(C.PAYOFF_MATRIX[self.action1_b][self.other_b_r1])
            else:
                self.room_payoff_r1 = cu(0)
        else:
            self.room_payoff_r1 = cu(0)

        self.participant.vars["ball_green_1"] = self.ball_green_r1
        self.participant.vars["room_payoff_1"] = self.room_payoff_r1

    other_b_r2 = models.BooleanField(doc="True (1) if co-player played B in round 2, else False (0).")
    room_payoff_r2 = models.CurrencyField(doc="Payoff for room 2, if selected for payment.")

    def draw_ball_r2(self):
        self.ball_green_r2 = random.random() < C.BALL_GREEN_PROBABILITY

    def draw_action_r2(self):
        self.other_b_r2 = random.random() < C.ACTION_B_PROBABILITY

    def calculate_payoff_r2(self):
        if self.other_b_r2 is not None:
            if self.ball_green_r2:
                self.room_payoff_r2 = cu(C.PAYOFF_MATRIX[self.action2_b][self.other_b_r2])
            else:
                self.room_payoff_r2 = cu(0)
        else:
            self.room_payoff_r2 = cu(0)

        self.participant.vars["ball_green_2"] = self.ball_green_r2
        self.participant.vars["room_payoff_2"] = self.room_payoff_r2

        if self.participant.vars.get('payment_room_1'):
            self.payoff = self.participant.vars["room_payoff_1"]
        else:
            self.payoff = self.room_payoff_r2

        self.participant.vars["payment"] = self.payoff

    # survey
    age = models.IntegerField(
        verbose_name='What is your age?',
        min=18, max=99,
        doc="Participant's age"
    )

    gender = models.StringField(
        choices=['Male', 'Female', 'Other', 'I prefer not to tell'],
        verbose_name='What is your gender?',
        widget=widgets.RadioSelect,
        doc="Participant's gender"
    )

    education = models.IntegerField(
        choices=[
            (0, 'Less than high school degree'),
            (1, 'High school degree or equivalent (e.g. GED)'),
            (2, 'Some college, but no degree'),
            (3, 'Associate degree'),
            (4, 'Bachelor degree'),
            (5, 'Graduate degree')
        ],
        verbose_name='What is the highest level of school you have completed or the highest degree you have received?',
        doc="Participant's level of education",
        widget=widgets.RadioSelect)

    major = models.StringField(
        verbose_name='If you had at least some college education, please tell us your major: ',
        blank=True,
        doc="Participant's major if they had at least some college education (education >= 3)"
    )

    risk = models.FloatField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        verbose_name='How do you see yourself: Are you in general a person who takes risk (10) or do you try to avoid \
                risks (0)? Please self-grade your choice (0-10).',
        widget=widgets.RadioSelectHorizontal(),
        doc="SOEP Risk question, scale 0 (lowest) to 10 (highest) propensity to take risk."
    )


def custom_export(players):
    # header row
    # yield ['idn', 'payment_round', 'payment']
    counter = 0
    for p in players:
        if not p.participant.visited or p.participant._index_in_pages < p.participant._max_page_index:
            continue
        counter += 1
        if p.payment_room_1:
            payment_round = 1
            if p.ball_green_r1:
                payment_passive = cu(C.PAYOFF_MATRIX[p.other_b_r1][p.action1_b])
            else:
                payment_passive = cu(0)
        else:
            payment_round = 2
            if p.ball_green_r2:
                payment_passive = cu(C.PAYOFF_MATRIX[p.other_b_r2][p.action2_b])
            else:
                payment_passive = cu(0)
        payment_passive = int(payment_passive)
        yield [counter, payment_round, payment_passive, p.session.code, p.participant.code]