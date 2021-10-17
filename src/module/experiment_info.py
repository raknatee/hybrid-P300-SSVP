from dataclasses import dataclass
import numpy as np
@dataclass(init=True)
class HeadsetInfo:
    sample_rate:float
    channel_names:list[str]

@dataclass(init=True)
class P300TimeInterval:
    after_p300_started:float
    end_time:float

@dataclass(init=True)
class P300ExperimentConfig:
    spawn:float
    ttl:float
@dataclass(init=True)
class ExperimentInfo:
    headset_info:HeadsetInfo
    p300_interval:P300TimeInterval
    p300_experiment_config:P300ExperimentConfig


ATTEMPT1 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7']),
                            p300_interval=P300TimeInterval(.2,.5),
                            p300_experiment_config=P300ExperimentConfig(.2,.2)
)

ATTEMPT2 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_interval=P300TimeInterval(.2,.5),
                            p300_experiment_config=P300ExperimentConfig(.2,.2)
)

THAILAND_POWER_LINE_FREQ = 50
def get_thailand_power_line_noise(experiment_info:ExperimentInfo)->np.ndarray:
    return np.arange(THAILAND_POWER_LINE_FREQ,experiment_info.headset_info.sample_rate/2,THAILAND_POWER_LINE_FREQ)
    