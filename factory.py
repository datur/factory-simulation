from src.worker import Worker
from src.factory import Factory

def solution():
    conveyor_length = 3
    processing_steps = 3

    workers = [[Worker(processing_steps), Worker(processing_steps)] for i in range(conveyor_length)]

    factory = Factory(conveyor_length, ["a", "b", None], workers)

    factory.simulate(100)

if __name__ == "__main__":
    solution()