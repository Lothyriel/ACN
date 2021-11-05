from enum import Enum


class ScanResult:
    def __init__(self, message, result):
        self.Result = result
        self.Message = message

    def __str__(self):
        return "{} | {}".format(self.Message, self.Result)


class EResult(Enum):
    OK = 0
    Regar = 1
    LandPobre = 2
    Mostra = 3
