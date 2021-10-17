from module.experiment_info import get_thailand_power_line_noise
from module.experiment_info import ATTEMPT2
import numpy as np
def test():
    assert np.equal(get_thailand_power_line_noise(ATTEMPT2),np.array([50,100])).all()
    