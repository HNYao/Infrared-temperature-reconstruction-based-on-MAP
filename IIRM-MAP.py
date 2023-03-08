from random import random
import numpy as np
import os
from IM import InfraredModel
class JMAP:
    def __int__(self, model: InfraredModel, criterion = 0.01, hp_mt = random(1),\
                hp_me =random(1)):
        '''

        :param model: InfraredModel
        :param criterion: the stopping criterion for gradient descent
        :param hp_mt: hyperparameter m_true
        :param hp_me:  hyperparameter m_e

        '''
        self.model = model
        self.criterion = criterion
        self.a_e = 1 + hp_me
        self.b_e = hp_me
        self.a_true = 1 + hp_me
        self.b_true = hp_me

        self.Temp_true = model.temp_m
        self.Temp_m = model.temp_m
        self.v_true = (self.b_true + pow(self.Temp_true, 2)/2)/(self.a_true + 1.5)
        self.v_e = (self.b_e + self.Temp_m - pow(self.model.forward(self.Temp_true), 2)/2)/(self.a_e + 1.5)

    def alternative_gd(self, step = 0.01) ->float :
        '''
        the alernative gradient descent in JMAP algorithm
        :param step: the step of gradient descent
        :return: true temperature through JMAP inference
        '''
        for i in range(100000):
            temp_true = temp_true - step * self.derative_cost

    @property
    def derative_cost(self):
        None

    @property
    def partial_deravative_h(self):
        None

    @property
    def h_function(self):
        None









