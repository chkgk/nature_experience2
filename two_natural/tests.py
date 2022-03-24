from otree.api import Currency as c, currency_range, Submission
from . import pages
from ._builtin import Bot
from .models import C
import random

class PlayerBot(Bot):

    def play_round(self):
        yield pages.Introduction
        yield pages.Instructions1
        c1 = {
            "c1_coplayer": C.COMPREHENSION_SOLUTIONS["c1_coplayer"], 
            "c2_probabilities": C.COMPREHENSION_SOLUTIONS["c2_probabilities"], 
            "c3_decision_importance": C.COMPREHENSION_SOLUTIONS["c3_decision_importance"]
        }
        yield pages.Comprehension1, c1
        yield pages.Comprehension1_check, c1

        c2 = {
            "c4_payoff_ab_red": C.COMPREHENSION_SOLUTIONS["c4_payoff_ab_red"], 
            "c5_payoff_ab_green": C.COMPREHENSION_SOLUTIONS["c5_payoff_ab_green"],
            "c6_payoff_bb_green": C.COMPREHENSION_SOLUTIONS["c6_payoff_bb_green"],
            "c7_payoff_ba_green": C.COMPREHENSION_SOLUTIONS["c7_payoff_ba_green"]
        }
        yield pages.Comprehension2, c2
        yield pages.Comprehension2_check, c2

        if self.player.aa_treatment:
            yield pages.ActionPreference, {"prefers_b": random.choice([True, False])}
            yield pages.DecisionInfo
            yield pages.DecisionAssignment
        else:
            yield pages.Decision1, {"action1_b": random.choice([True, False])}

        yield pages.Belief_color1, {"green_red_r1": random.randint(0, 100)}
        yield pages.Belief_other1, {"a_or_b_r1": random.randint(0, 100)}
        yield Submission(pages.Match1, check_html=False)
        yield pages.Results1
        yield pages.Decision2, {"action2_b": random.choice([True, False])}
        yield pages.Belief_color2, {"green_red_r2": random.randint(0, 100)}
        yield pages.Belief_other2, {"a_or_b_r2": random.randint(0, 100)}
        yield pages.Motivation, {"motivation": random.randint(1,5), "motivation_other": ""}
        yield Submission(pages.Match2, check_html=False)
        yield pages.Results2

        edu_num = random.randint(0, 5)
        if edu_num >= 2:
            edu_major = "Economics"
        else:
            edu_major = ""
        yield pages.Survey, {
            'age': random.randint(18,99), 
            'gender': random.choice(['Male', 'Female', 'Other', 'I prefer not to tell']), 
            'education': edu_num, 
            'major': edu_major, 
            'risk': random.randint(0,10)
        }
        yield pages.LastPage

