from torch.utils.data import Dataset
from .get_dataset import P300Data

class P300Dataset(Dataset):
    def __init__(self,data:list[P300Data]) -> None:
        super().__init__()
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index) -> dict:
        return {
            "target": 1 if self.data[index].target else 0,
            "eeg": self.data[index].eeg
        }