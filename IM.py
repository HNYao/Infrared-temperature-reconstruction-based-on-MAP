import numpy as np


class InfraredModel:
    def __int__(self, temp_true, temp_m, temp_u, temp_a, h, ac, dist, em=0.97, sensor=4.09):
        '''

        :param temp_true: the true temperature
        :param temp_m:  the measuring temperature
        :param temp_u:  the temperature of background
        :param temp_a: the temperature of atmosphere
        :param h: the relative humidity
        :param ac: the attenuation coefficient
        :param dist: the measuring distance
        :param em: the emissivity
        :param sensor: the sensor coefficient, generally equal to 4.09
        '''

        self.temp_t = temp_true
        self.temp_m = temp_m
        self.temp_u = temp_u
        self.temp_a = temp_a
        self.hum = h
        self.au_co = self.humidity(self.hum)
        self.sensor_co = sensor
        self.em_co = em
        self.dist = dist

    def forward(self, temp_true):
        """
        calculate the measuring temperature based on the infrared model

        :param temp_true: the true temperature, float
        :return: the measuring temperature, float
        """
        temp_item = self.em_co * temp_true + (1 - self.em_co) * pow(self.temp_u, self.sensor_co) + \
                     (np.exp(self.au_co * self.dist) - 1) * pow(self.temp_a, self.sensor_co)
        domin_item = np.exp(self.hum * self.dist)

        return pow(temp_item/domin_item, 1/self.sensor_co)

    def backward(self, temp_meas):
        """
        calculate the true temperature

        :param temp_meas: the measuring temperature, float
        :return: the measuring temperature, float
        """
        temp_item = np.exp(self.au_co * self.dist) * pow(temp_meas, self.sensor_co) - (1 - self.em_co) * \
                     pow(self.temp_u, self.sensor_co) - (np.exp(self.au_co * self.dist) - 1) * \
                     pow(self.temp_a, self.sensor_co)
        domin_item = self.em_co

        return pow(temp_item/domin_item, 1/self.sensor_co)

    def humidity(self, humidity):
        """
        :param humidity: the relative humidity
        :return: attenuation coefficient parameter
        """
        return humidity / 100 * 0.084