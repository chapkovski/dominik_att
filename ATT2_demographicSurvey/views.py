from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Demographics(Page):

    form_model = models.Player

    form_fields = ['age','gender','state','race']

    def before_next_page(self):
        self.player.participant.vars['gender'] = self.player.gender

page_sequence = [
    Demographics,
]
