from dataclasses import dataclass
import numpy as np
@dataclass(init=True)
class HeadsetInfo:
    sample_rate:float
    channel_names:list[str]



@dataclass(init=True)
class P300ExperimentConfig:
    spawn:float
    ttl:float
@dataclass(init=True)
class ExperimentInfo:
    headset_info:HeadsetInfo
    p300_experiment_config:P300ExperimentConfig


ATTEMPT1 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7']),
                            p300_experiment_config=P300ExperimentConfig(.2,.2)
)

ATTEMPT2 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(.2,.2)
)

ATTEMPT3 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(0,.8)
)

ATTEMPT4 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(.1,.2)
)

ATTEMPT5 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(0,1)
)

ATTEMPT6 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(0,1)
)

ATTEMPT7 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(.1,.2)
)

ATTEMPT8 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(0,2)
)

ATTEMPT11 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(0,1))
                          
ATTEMPT12 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(0,1))
                            
ATTEMPT13 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(.1,.2))

ATTEMPT14 = ExperimentInfo(headset_info=HeadsetInfo(230,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(.3,.6))

ATTEMPT15 = ExperimentInfo(headset_info=HeadsetInfo(240,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(.3,.6))

ATTEMPT16 = ExperimentInfo(headset_info=HeadsetInfo(250,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(0,1))

THAILAND_POWER_LINE_FREQ = 50
def get_thailand_power_line_noise(experiment_info:ExperimentInfo)->np.ndarray:
    return np.arange(THAILAND_POWER_LINE_FREQ,experiment_info.headset_info.sample_rate/2,THAILAND_POWER_LINE_FREQ)
    