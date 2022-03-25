from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import C


class Introduction(Page):
    pass


class Instructions1(Page):
    def before_next_page(self):
        self.player.get_payment_data()


class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']


class LastPage(Page):
    def vars_for_template(self):
        return {
            'experimenter_name': self.session.config.get('experimenter_name', 'Christian Koenig'),
            'experimenter_email': self.session.config.get('experimenter_email', 'christian.koenig@uibk.ac.at')
        }


page_sequence = [Introduction, Instructions1, Survey, LastPage]
