from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
import math
import time
from otree_mturk_utils.views import CustomMturkPage, CustomMturkWaitPage

class GroupingWaitpage(CustomMturkWaitPage):
    group_by_arrival_time = True
    use_task = False 
    startwp_timer = 300
    template_name = 'ATT2_gender/GroupingWaitpage.html'
  
    def vars_for_template(self):
        for p in self.subsession.get_players():
            p.participant.vars['role'] = p.role
            
        players_in_game = [p for p in self.subsession.get_players() if p.participant.vars['consented'] == 'yes']
        num_players_in_game = len(players_in_game)                       
        return {
            'num_players_in_game' : num_players_in_game,
            'num_players' : Constants.num_players
        }
        
    def get_players_for_group(self, waiting_players):
        if self.subsession.round_number == 1:
            newest_player = waiting_players[-1]
            possible_partners = waiting_players[:-1]
            if len(possible_partners) >= Constants.players_per_group-1:
                return possible_partners[:Constants.players_per_group-1 ] + [newest_player] 
            matrix = self.subsession.get_group_matrix()
            print('Matrix"', matrix)
             
        if self.subsession.round_number == 2:
            newest_player = []
            already_waiting = []
            newest_player = waiting_players[-1]
            already_waiting = waiting_players[:-1]
            possible_partners = [p for p in already_waiting if 
                p.participant.vars['role'] != newest_player.participant.vars['role'] and 
                p.in_round(1).group != newest_player.in_round(1).group]
            if len(possible_partners) >= Constants.players_per_group-1:
                return possible_partners[:Constants.players_per_group-1 ] + [newest_player] 
            matrix = self.subsession.get_group_matrix()
            print('Matrix"', matrix)    
            
        if self.subsession.round_number == 3:
            newest_player = []
            already_waiting = []
            newest_player = waiting_players[-1]
            already_waiting = waiting_players[:-1]
            possible_partners = [p for p in already_waiting if 
                p.participant.vars['role'] != newest_player.participant.vars['role'] and 
                p.in_round(1).group != newest_player.in_round(1).group and 
                p.in_round(2).group != newest_player.in_round(2).group]
            if len(possible_partners) >= Constants.players_per_group-1:
                return possible_partners[:Constants.players_per_group-1 ] + [newest_player]            
            matrix = self.subsession.get_group_matrix()
            print('Matrix"', matrix)
             
class Demographics(CustomMturkPage):
    form_model = models.Player
    form_fields = ['age','gender','state','race']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def before_next_page(self):
        self.player.participant.vars['gender'] = self.player.gender
                
class Introduction(CustomMturkPage):
    timeout_seconds = 300
    
    def is_displayed(self):
        return self.subsession.round_number == 1
    
    def vars_for_template(self):                
        return {
            'num_rounds': Constants.num_rounds
        }
            
class IntroductionWaitpage(CustomMturkWaitPage):
    use_task = False
    template_name = 'ATT2_gender/IntroductionWaitpage.html'
            
    def is_displayed(self):
        return self.subsession.round_number == 1 
               
class Screen1(CustomMturkPage):
    timeout_seconds = 120
                   
    def vars_for_template(self):
        self.player.gender = self.player.participant.vars['gender']
        
        for p in self.group.get_players():
            if p.id_in_group  == 1:
                if p.gender == 0:
                    self.group.gender_p1 = 'Male'
                elif p.gender == 1:
                    self.group.gender_p1 = 'Female'
            elif p.id_in_group  == 2:
                if p.gender == 0:
                    self.group.gender_p2 = 'Male'
                elif p.gender == 1:
                    self.group.gender_p2 = 'Female'        

        for p in self.group.get_players():
            if p.id_in_group  == 1:
                p.other_gender = self.group.gender_p2
            elif p.id_in_group  == 2:
                p.other_gender = self.group.gender_p1
                
        self.group.special_number = random.randint(1, 3)
        self.group.bump_number = random.randrange(0, 2) - 1   
            
        return {
            'role': self.player.role,
            'special_number': self.group.special_number,
            'round': self.subsession.round_number,
            'num_rounds': Constants.num_rounds,
        }

class Screen1Waitpage(CustomMturkWaitPage):
    use_task = False
    template_name = 'ATT2_gender/Screen1Waitpage.html'
    def after_all_players_arrive(self):
        pass
        
class Screen2(CustomMturkPage):
    form_model = models.Group
    form_fields = ['demand','effort','demandArray','effortArray']

    timeout_seconds = 120
      
    def vars_for_template(self):                
        return {
            'role': self.player.role,
            'special_number': self.group.special_number,
            'other_gender': self.player.other_gender,
        }
        
    def is_displayed(self):
        return self.player.id_in_group == 1

    def before_next_page(self):
        if self.timeout_happened:
            self.group.demand = random.randint(1,7)
            self.group.effort = random.randint(1,3)
            
        if self.participant._is_bot == 1:
            self.group.demand = random.randint(1,7)
            self.group.effort = random.randint(1,3)
        
class Screen2Waitpage(CustomMturkWaitPage):
    use_task = False
    template_name = 'ATT2_gender/Screen2Waitpage.html'
    def after_all_players_arrive(self):
        pass    
        
class Screen3(CustomMturkPage):
    form_model = models.Group
    form_fields = ['choice','bonus']

    timeout_seconds = 120 

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        self.group.choice_outcome = self.group.effort + self.group.special_number + self.group.bump_number   
        role = self.player.role
        choice_outcome = self.group.choice_outcome
        return {
            'role': role,
            'choice': self.group.choice,
            'bonus': self.group.bonus,
            'choice_outcome': choice_outcome,
            'other_gender': self.player.other_gender
        }

    def before_next_page(self):
        if self.timeout_happened:
            self.group.choice = random.randint(0,1)
            self.group.bonus = random.randint(0,1)
            
        if self.participant._is_bot == 1:
            self.group.choice = random.randint(0,1)
            self.group.bonus = random.randint(0,1)
            
class Screen3Waitpage(CustomMturkWaitPage):
    use_task = False
    template_name = 'ATT2_gender/Screen3Waitpage.html'
    def after_all_players_arrive(self):
        pass
            
class Screen4(CustomMturkPage):
    timeout_seconds = 60
        
    def vars_for_template(self):           
        self.group.increased_choice_outcome = (self.group.choice_outcome + 
            (self.group.effort * self.group.choice) + (self.group.special_number * (1 - self.group.choice)))
        
        if self.player.id_in_group == 1:
            if self.group.bonus == 0:
                self.player.payoff = (c((6 * math.sqrt(self.group.choice_outcome) - 
                    self.group.effort* 1.95)).to_real_world_currency(self.session))
            elif self.group.bonus == 1:    
                self.player.payoff = (c((6 * math.sqrt(self.group.choice_outcome + 1) - 
                    self.group.effort* 1.95)).to_real_world_currency(self.session))    
        elif self.player.id_in_group == 2:
            self.player.payoff = c(self.group.increased_choice_outcome).to_real_world_currency(self.session)
                
        return {
            'special_number': self.group.special_number,
            'effort': self.group.effort,
            'choice_outcome': self.group.choice_outcome,
            'increased_choice_outcome': self.group.increased_choice_outcome,
            'bonus': self.group.bonus,
            'payoff': self.player.payoff,
            'role': self.player.role,
            'round': self.subsession.round_number,
            'num_rounds': Constants.num_rounds
        }
        
class Results(CustomMturkPage):
    timeout_seconds = 60
    
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds
        
    def vars_for_template(self):
        self.player.round_chosen_payoff = random.randint(1,Constants.num_rounds)
        round_chosen_payoff = self.player.round_chosen_payoff
        self.player.chosen_payoff = self.player.in_round(self.player.round_chosen_payoff).payoff
        if self.subsession.round_number == Constants.num_rounds:
            self.player.total_payoff = self.session.config['participation_fee'] + self.player.chosen_payoff
        return {
            'chosen_payoff': self.player.chosen_payoff,
            'total_payoff': self.player.total_payoff
        }

page_sequence = [
    GroupingWaitpage,
    Demographics,
    Introduction,
    IntroductionWaitpage,
    Screen1,
    Screen1Waitpage,
    Screen2,
    Screen2Waitpage,
    Screen3,
    Screen3Waitpage,
    Screen4,
    Results
]
