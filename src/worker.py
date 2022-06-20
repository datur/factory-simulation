
import string
from typing import Any, Tuple


class Worker:
    """
    A class to represent a factory worker.

    Args:
    Processing Steps: int
        Configurable number of steps it takes to complete the
        item currently assigned

    """
    def __init__(self, processing_steps: int = 3):
        """Constructor

        Args:
            processing_steps (int, optional): Number of processing stepsto complete assigned item.
            Defaults to 3.
        """
        self.available: bool = True
        self.work_left: int = 0
        self.work_item = None
        self.processing_steps = processing_steps


    def do_work(self):
        """
        Method to represent the workers performing a work action.
        Essentially decreases the reemaining work for the worker by 1.
        """
        self.work_left -= 1 if self.work_left > 0 else 0


    def assign_work(self, item: Any):
        """
        Assigns a work item to the worker

        Args:
        item: Any
            An item for the worker to work on
        """
        self.work_left = self.processing_steps
        self.available = False
        self.work_item = item

    def complete_work(self) -> Tuple[str, Any]:
        """
        Completes a piece of work and returns comleted item
        """
        completed_work_item = self.work_item
        self.work_item = None
        self.available = True

        return ("Completed", completed_work_item)

    def __iter__(self):
        # Used in debugging
        yield "available", self.available,
        yield "work_left", self.work_left,
        yield "work_item", self.work_item,