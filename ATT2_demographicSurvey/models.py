from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json, 
)
import csv
import random
import math

from django import forms
from localflavor.us.models import USStateField

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'ATT2_demographicSurvey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    role = random.randint(1,2)
    
    age = models.PositiveIntegerField(verbose_name='How old are you?')

    gender = models.PositiveIntegerField(initial=None, choices=[(0, 'male'),
                                                               (1, 'female'),
                                                                (7, 'other')],
                                         verbose_name='What is your gender?',
                                                                widget=widgets.Select())
    state = USStateField(
        verbose_name='Which is your state of residence?',blank=True)

    race = models.PositiveIntegerField(initial=None,
                                       choices=[(1, 'White Non-Hispanic'),
                                                (2, 'Black Non-Hispanic'),
                                                (3, 'Hispanic'),
                                                (99, 'Other or multiple races, Non-Hispanic'),],
                                       verbose_name='What is your race or ethnicity?',
                                       widget=widgets.RadioSelect)
