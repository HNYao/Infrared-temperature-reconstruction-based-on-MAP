import numpy as np
class InfraredModel:
    def __int__(self, tt, tm, tu, ta, h, ac, dist, em = 0.97, sensor = 4.09):
        self.temp_t = tt
        self.temp_m = tm
        self.temp_u = tu
        self.temp_a = ta
        self.hum = h
        self.au_co = ac
        self.sensor_co = sensor
        self.em_co = em
        self.dist = dist

    def forward(self, temp_true):
        """
        calculate the measuring temperature based on the infrared model

        :parem temp_true: the true temperature, floart
        :return: the measuring temperature, float
        """
        temp_iterm = self.em_co * temp_true + (1 - self.em_co) * pow(self.temp_u, self.sensor_co) + \
                     (np.exp(self.au_co * self.dist) - 1) * pow(self.temp_a, self.sensor_co)
        domin_iterm = np.exp(self.hum * self.dist)

        return pow(temp_iterm/domin_iterm, 1/self.sensor_co)

    def backward(self, temp_meas):
        """

        :param temp_meas: the measuring temperature, float
        :return: the measuring temperature, float
        """
        temp_iterm =