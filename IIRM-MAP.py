from random import random
import numpy as np
import os
from IM import InfraredModel


class JMAP:
    def __int__(self, model: InfraredModel, criterion=0.01, hp_mt=random(),
                hp_me =random()):
        '''
        Use JMAP algorithm to reconstruct the true temperature from the measuring temperature
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

        self.temp_true = model.temp_m
        self.temp_m = model.temp_m
        self.v_true = (self.b_true + pow(self.temp_true, 2)/2)/(self.a_true + 1.5)
        self.v_e = (self.b_e + self.temp_m - pow(self.model.forward(self.temp_true), 2)/2)/(self.a_e + 1.5)

    def alternative_gd(self, step=0.01) ->float:

        '''
        the alternative gradient descent in JMAP algorithm
        :param step: the step of gradient descent
        :return: true temperature through JMAP inference
        '''

        em = self.model.em_co
        dist = self.model.dist
        hum = self.model.hum
        temp_u = self.model.temp_u
        temp_a = self.model.temp_a
        sensor = self.model.sensor_co

        temp_true = self.temp_true
        temp_m = self.temp_m
        b_true = self.b_true
        a_true = self.a_true
        v_e = self.v_e
        v_true = self.v_true
        b_e= self.b_e
        a_e = self.a_e
        for i in range(100000):
            temp_true = temp_true - step * self.derivative_cost(temp_true, v_true, em, dist,
                                                              hum, temp_u, temp_a, sensor)
            b_true +=  temp_true * temp_true / 2
            a_true += 1.5
            v_true = b_true / a_true

            b_e = b_e + pow((temp_m - self.h_function(temp_true, em, dist, hum, temp_u, sensor, temp_a)), 2)/2
            a_e = a_e + 1.5
            v_e = b_e / a_e

        return temp_true


    def derivative_cost(self, temp_true, v_true, em, dist, hum, temp_u, temp_a, sensor) ->float:
        """
        the derivative of the cost function
        :param temp_true: the true temperature
        :param em: the emissivity
        :param dist: the distance
        :param hum: the humidity
        :param temp_u: the temperature of background
        :param temp_a: the temperature of atmosphere
        :param sensor: the sensor coefficient
        :return: the derivative of the cost function, float
        """
        result = self.partial_deravative_h(temp_true, em, dist, hum, temp_u, sensor, temp_a) *\
            self.h_function(temp_true, em, dist, hum, sensor, temp_a) / v_true

        return result


    def partial_derivative_h(self, temp_true, em, dist, hum, temp_u, sensor, temp_a) ->float:

        '''
        the partial derivative of function h
        :param temp_true: the true temperature
        :param em: the emissivity
        :param dist: the measuring distance
        :param hum: humidity coefficient
        :param temp_u: the background temperature
        :param sensor: the sensor coefficient
        :param temp_a:  the temperature of atmosphere
        :return: partial derivative of h, float
        '''

        item1 = (1 / sensor) * ((1 / np.exp(hum * dist))) * (em * pow(temp_true, sensor))
        item2= (1 - em) * pow(temp_u, sensor) + pow((np.exp(hum * dist) - 1) * pow(temp_a, sensor), (1/(sensor - 1))) * \
                                                    (sensor * em / np.exp(hum * dist)) * pow(temp_true, sensor - 1)
        return item1 + item2


    def h_function(self, temp_true, em, dist, hum, temp_u, sensor, temp_a) ->float:

        '''
        function h, the inverse version of the InfraredModel.forward
        :param temp_true: the true temperature
        :param em: the emissivity
        :param dist: the measuring distance
        :param hum: the humidity
        :param temp_u: the temperature of background
        :param sensor: the sensor coefficient
        :param temp_a: the temperature of atmosphere
        :return: float
        '''

        item1 = (1 / np.exp(hum * dist))* (em * pow(temp_true, sensor) + (1- em) * pow(temp_u, sensor))
        item2 = pow((np.exp(hum * dist) - 1) * pow(temp_a, sensor), 1 / sensor)

        return item1 + item2










