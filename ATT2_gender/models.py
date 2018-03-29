from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json, 
)

import csv
import itertools
import random
import math

from django import forms
from localflavor.us.models import USStateField
from decimal import Decimal

author = 'Your name here'

doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'ATT2_gender'
    players_per_group = 2
    num_rounds = 3
    num_players = 6

class Subsession(BaseSubsession): 
    def creating_session(self):
         self.group_randomly(fixed_id_in_group=True)
                                        
class Group(BaseGroup):
    special_number = models.IntegerField(initial=0,)

    bump_number = models.IntegerField(initial=0,)

    demand = models.PositiveIntegerField(choices=(1,2,3,4,5,6,7),widget=widgets.RadioSelectHorizontal())                                    
    
    demandArray = models.CharField()
    
    effort = models.PositiveIntegerField(choices=(1,2,3),widget=widgets.RadioSelectHorizontal())

    effortArray = models.CharField()

    choice = models.IntegerField(choices=[(0, 'Special Number Higher'), (1, 'Effort Higher'),],
            widget=widgets.RadioSelectHorizontal())

    choice_outcome = models.IntegerField()

    increased_choice_outcome = models.IntegerField()

    bonus = models.IntegerField(choices=[(0, 'No Bonus'), (1, 'Bonus'),], 
        widget=widgets.RadioSelectHorizontal())
    
    gender_p1 = models.CharField()
    
    gender_p2 = models.CharField()

class Player(BasePlayer):     
    def role(self):
        if self.subsession.round_number == 1:
            if self.id_in_group == 1:
                return 'Player 1'
            else: 
                return 'Player 2'
        else:
            if self.in_round(1).id_in_group == 1:
                return 'Player 1'
            elif self.in_round(1).id_in_group == 2:
                return 'Player 2'

    age = models.PositiveIntegerField(verbose_name='How old are you?')

    gender = models.PositiveIntegerField(initial=None, choices=[(0, 'male'),
                                                               (1, 'female')],
                                                                # (7, 'other')],
                                         verbose_name='What is your gender?',
                                         widget=widgets.RadioSelect())
    state = USStateField(
        verbose_name='Which is your state of residence?',blank=True)

    race = models.PositiveIntegerField(initial=None,
                                       choices=[(1, 'White Non-Hispanic'),
                                                (2, 'Black Non-Hispanic'),
                                                (3, 'Hispanic'),
                                                (4, 'Other or multiple races, Non-Hispanic'),],
                                       verbose_name='What is your race or ethnicity?',
                                       widget=widgets.RadioSelect)


    round_chosen_payoff = models.IntegerField(initial=1,)

    chosen_payoff = models.DecimalField(max_digits=5, decimal_places=2)

    total_payoff = models.DecimalField(max_digits=5, decimal_places=2)

    other_gender = models.CharField()
    