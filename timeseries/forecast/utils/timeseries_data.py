import os
from abc import ABC
from abc import abstractmethod

default_dir_path = "data"


class TimeSeriesData(ABC):

    def __init__(self, data_type, data_name, dirpath=default_dir_path):
        self.dirpath = dirpath
        self.data_type = data_type
        self.data_name = data_name
        self.ts = None
        self.train_interval = None
        self.val_interval = None
        self.test_interval = None
        self.pred_steps = None
        self.pred_jump = None
        self.load()

    def load(self):
        if not os.path.isdir(self.dirpath):
            raise Exception(f"Dictionary '{self.dirpath}' does not exist")
        self.__load__()
        assert self.ts is not None
        self.__set_competition_params__()
        assert self.train_interval is not None
        assert self.val_interval is not None
        assert self.test_interval is not None
        assert self.pred_steps is not None
        assert self.pred_jump is not None

    @abstractmethod
    def __load__(self):
        ...

    @abstractmethod
    def __set_competition_params__(self):
        ...


# class NewClassName(TimeSeriesData):

#     def __init__(self, dirpath=default_dir_path):
#         super().__init__("", "", dirpath)

#     def __load__(self):


#     def __set_competition_params__(self):
