from collections import deque, Counter
from textwrap import dedent
import random
from typing import Any, List, Tuple
from .worker import Worker



class Factory:
    """
    A class to represent a factory.
    ```
        v   v   v   v   v          workers
        ---------------------
    -> | A |   | B | A | P | ->     conveyor belt
        ---------------------
        ^   ^   ^   ^   ^          workers
    ```
    Args:
    conveyor_belt_length : int
        The length of the factorys conveyor belt
    conveyor_belt_options : List[Any]
        A list of options that can be added to the conveyor belt to work on
        eg ["a", "Some Item", object]
    workers : List[Tuple|List[Worker, ...]]
        A List of a List of workers equal to the length of the conveyor belt.
    """
    def __init__(self, conveyor_belt_length: int, conveyor_belt_options: List[Any], workers: List[Tuple[Worker, ...]]):
        """
        Constructor

        Args:
        conveyor_belt_length : int
            The length of the factorys conveyor belt
        conveyor_belt_options : List[Any]
            A list of options that can be added to the conveyor belt to work on
            eg ["a", "Some Item", object]
        workers : List[Tuple|List[Worker, ...]]
            A List of a List of workers equal to the length of the conveyor belt.
        """
        self.conveyor_belt = deque([None for _ in range(conveyor_belt_length)], conveyor_belt_length)
        self.workers = workers
        self.retults = []

        # Add none to the product options to represent an empty slot
        if None not in conveyor_belt_options:
            conveyor_belt_options.append(None)

        self.conveyor_belt_options = conveyor_belt_options
        self.conveyor_belt_valid_options = [x for x in conveyor_belt_options if x is not None]

    def add_item_to_conveyor(self):
        """
        Adds a new item to the factorys conveyorbelt at random.
        The choice is from n in conveyor_belt_valid_options
        """
        discard = self.conveyor_belt[0]
        self.retults.append(discard)
        next_item = random.choice(self.conveyor_belt_options)
        self.conveyor_belt.append(next_item)

    def worker_item_pick(self):
        for position, i in zip(self.conveyor_belt, range((len(self.conveyor_belt)))):

            # If the current item in the queue is a valid coice
            if position in self.conveyor_belt_valid_options:

                available_workers = [w for w in self.workers[i] if w.available]


                if len(available_workers) > 0:

                    chosen_worker = random.choice(available_workers) if len(available_workers) > 1 else available_workers[0]

                    chosen_worker.assign_work(position)

                    # remove item from deque
                    self.conveyor_belt[i] = None

            elif position not in self.conveyor_belt_valid_options:

                # if the conveyorbelt is empty then check for any workers that are currently
                # not available to see if they are complete with their work

                unavailable_workers = [w for w in self.workers[i] if not w.available and w.work_left == 0]

                if len(unavailable_workers) > 0:

                    worker_complete = random.choice(unavailable_workers) if len(unavailable_workers) > 1 else unavailable_workers[0]

                    self.conveyor_belt[i] = worker_complete.complete_work()


    def workers_do_work(self):
        """
        Have each worker at each position do work
        """
        # [[worker.do_work() for worker in worker_position] for worker_position in self.workers]
        for pair in self.workers:
            for worker in pair:
                worker.do_work()

    def process(self):
        """
        A full step in manufacture:
            Add item to conveyor belt
            Assign work item or place completed item back
            Workers do work
        """
        self.add_item_to_conveyor()
        self.worker_item_pick()
        self.workers_do_work()

    def simulate(self, n: int):
        """Simulate a given number of processing steps

        Args:
            n (int): Number of processing steps
        """
        for _ in range(n):
            self.process()
        report = dict(Counter(self.retults))

        result = "\n".join(f"Item: {k} Count: {v}" for k, v in report.items())
        print(f"""Processed items over {n} steps:\n{result}""")
