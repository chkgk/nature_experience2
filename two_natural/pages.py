from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import C

class Introduction(Page):
    pass

class Instructions1(Page):
    pass

class Comprehension1(Page):
    form_model = "player"
    form_fields = ["c1_coplayer", "c2_partner", "c3_probabilities", "c4_decision_importance"]

    def vars_for_template(self):
        return {
            'c1_solution': C.COMPREHENSION_SOLUTIONS['c1_coplayer'],
            'c2_solution': C.COMPREHENSION_SOLUTIONS['c2_partner'],
            'c3_solution': C.COMPREHENSION_SOLUTIONS['c3_probabilities'],
            'c4_solution': C.COMPREHENSION_SOLUTIONS['c4_decision_importance'],
        }


class Comprehension2(Page):
    form_model = "player"
    form_fields = ["c5_payoff_ab_red", "c6_payoff_ab_green", "c7_payoff_bb_green", "c8_payoff_ba_green"]

    def vars_for_template(self):
        return {
            'c5_solution': C.COMPREHENSION_SOLUTIONS["c5_payoff_ab_red"],
            'c6_solution': C.COMPREHENSION_SOLUTIONS["c6_payoff_ab_green"],
            'c7_solution':C.COMPREHENSION_SOLUTIONS["c7_payoff_bb_green"],
            'c8_solution': C.COMPREHENSION_SOLUTIONS["c8_payoff_ba_green"],
        }


class ActionPreference(Page):
    def is_displayed(self):
        return self.player.aa_treatment

    form_model = 'player'
    form_fields = ["prefers_b"]


class DecisionInfo(Page):
    def is_displayed(self):
        return self.player.aa_treatment

class DecisionAssignment(Page):
    def is_displayed(self):
        return self.player.aa_treatment

    def before_next_page(self):
        self.player.action1_b = True
        self.player.set_participant_var()

class Decision1(Page):
    def is_displayed(self):
        return self.player.ra_treatment

    form_model = 'player'
    form_fields = ['action1_b']

    def before_next_page(self):
        self.player.set_participant_var()


class Belief_color1(Page):
    form_model = 'player'
    form_fields = ['green_red_r1']


class Belief_other1(Page):
    form_model = 'player'
    form_fields = ['a_or_b_r1']


class Match1(Page):
    timeout_seconds = C.MIN_WAIT

    def vars_for_template(self):
        return {
            "title_text": "Please wait!"
        }

    def before_next_page(self):
        self.player.draw_ball_r1()
        self.player.draw_action_r1()
        self.player.calculate_payoff_r1()


class Decision2(Page):
    form_model = 'player'
    form_fields = ['action2_b']

    def before_next_page(self):
        self.player.determine_switch()

class Belief_color2(Page):
    form_model = 'player'
    form_fields = ['green_red_r2']


class Belief_other2(Page):
    form_model = 'player'
    form_fields = ['a_or_b_r2']


class Match2(Page):
    timeout_seconds = C.MIN_WAIT

    def vars_for_template(self):
        return {
            "title_text": "Please wait!"
        }

    def before_next_page(self):
        self.player.draw_ball_r2()
        self.player.draw_action_r2()
        self.player.calculate_payoff_r2()

class Results1(Page):
    def vars_for_template(self):
        return {
            'own_action': 'B' if self.player.action1_b else 'A',
            'others_action': 'B' if self.player.other_b_r1 else 'A',
            'ball_color': 'green' if self.player.ball_green_r1 else 'red',
        }

class Results2(Page):
    def vars_for_template(self):
        return {
            'own_action': 'B' if self.player.action2_b else 'A',
            'others_action': 'B' if self.player.other_b_r2 else 'A',
            'ball_color': 'green' if self.player.ball_green_r2 else 'red',
        }
    
class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'major', 'risk']

    def error_message(self, values):
        if values["education"] >= 2 and (values["major"] == " " or values["major"] is None):
            return "Please indicate your major."


class LastPage(Page):
    def vars_for_template(self):
        return {
            'payment_room': '1' if self.player.participant.vars.get('payment_room_1', None) else '2',
            'payment': self.player.participant.vars.get('payment', None),
            'experimenter_name': self.session.config.get('experimenter_name', 'Christian Koenig'),
            'experimenter_email': self.session.config.get('experimenter_email', 'christian.koenig@uibk.ac.at')
        }


page_sequence = [
    Introduction,
    Instructions1,
    Comprehension1,
    Comprehension2,
    ActionPreference,
    DecisionInfo,
    DecisionAssignment,
    Decision1,
    Belief_color1,
    Belief_other1,
    Match1,
    Results1,
    Decision2,
    Belief_color2,
    Belief_other2,
    Match2,
    Results2,
    Survey,
    LastPage
]