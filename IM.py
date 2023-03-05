import numpy as np
class InfraredModel:
    def __int__(self, tt, tm, tu, ta, h, ac, dist, em = 0.97, sensor = 4.09):
        self.temp_t = tt
        self.temp_m = tm
        self.temp_u = tu
        self.temp_a = ta
        self.hum = h
        self.au_co = self.humity(self.hum)
        self.sensor_co = sensor
        self.em_co = em
        self.dist = dist

    def forward(self, temp_true):
        """
        calculate the measuring temperature based on the infrared model

        :parem temp_true: the true temperature, floart
        :return: the measuring temperature, float
        """
        temp_item = self.em_co * temp_true + (1 - self.em_co) * pow(self.temp_u, self.sensor_co) + \
                     (np.exp(self.au_co * self.dist) - 1) * pow(self.temp_a, self.sensor_co)
        domin_item = np.exp(self.hum * self.dist)

        return pow(temp_item/domin_item, 1/self.sensor_co)

    def backward(self, temp_meas):
        """

        :param temp_meas: the measuring temperature, float
        :return: the measuring temperature, float
        """
        temp_item = np.exp(self.au_co * self.dist) * pow(temp_meas, self.sensor_co) - (1 - self.em_co) * \
                     pow(self.temp_u, self.sensor_co) - (np.exp(self.au_co * self.dist) - 1) * \
                     pow(self.temp_a, self.sensor_co)
        domin_item = self.em_co

        return pow(temp_item/domin_item, 1/self.sensor_co)

    def humity(self, humity):
        """
        :param humity: the relative humity
        :return: autenuation coefficient parameter
        """
        return humity / 100 * 0.084