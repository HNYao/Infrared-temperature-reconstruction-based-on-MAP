import numpy as np
import os
from IM import InfraredModel
class JMAP:
    def __int__(self, model: InfraredModel, criterion = 0.01, hp_a = 0.5,\
                ):
        self