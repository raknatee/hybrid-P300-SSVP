from torch import Tensor
  
def to_one_hot(y:Tensor)->list[int]:
    return (list(map(int,(y>.5).flatten().tolist())))

def acc(y_true:list[int],y_hat:list[int])->float:
    assert len(y_true) == len(y_hat)
    correct:int = 0

    for i in range(len(y_true)):
        if(y_true[i] == y_hat[i]):
            correct +=1
  
    return correct/len(y_true)
    