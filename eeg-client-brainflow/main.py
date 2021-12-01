import brainflow #type:ignore
from brainflow.board_shim import BoardShim, BrainFlowInputParams #type:ignore
import time
from datetime import datetime


import numpy as np
from numpy import ndarray
def main(): 

    connector:BrainFlowInputParams = BrainFlowInputParams()
    connector.serial_port = "COM3"

    # for Cyton, board_id = 0 
    board = BoardShim(0,connector)
    
    board.prepare_session()
    board.start_stream()
    print("start")
    index = 0
    with open("data.txt","w") as output_file:
        while True:
            
            # if(board.get_board_data_count()>0):
            data:ndarray = board.get_board_data()
            # data shape => (24, sample)

            # if(data.shape[1]>250):
            #     print("found")
            #     ok_samples:list[int] = []
            #     for sample in range(data.shape[1]):
            #         sample_sum:float = data[:,sample].sum()
            #         output_file.write(f"{str(data[:,sample])}\n")
            #         if(sample_sum!=0):
            #             ok_samples.append(sample)
            #     data[:,ok_samples]

            # if(data.shape[1]>250):
            #     print(f"{index} {data.shape} <<<<")
            # else:
            #     print(f"{index} {data.shape}")


            output_file.write(f"ts by com: {datetime.now().timestamp()}")
            output_file.write(f"\n {data.shape=}")
            output_file.write("\n"+'-'*20+"\n")

            time.sleep(1/250)
            index+=1
     
     


if __name__ == "__main__":
    main()