from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Consent(Page):
    template_name = 'consent/consent.html'
    
    def before_next_page(self):
        self.player.consented = 'yes'
        for p in self.subsession.get_players():
            p.participant.vars['consented'] = p.consented
                
page_sequence = [
    Consent
]
