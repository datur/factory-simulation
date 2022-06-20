from collections import deque
from typing import Tuple
import pytest

from src.factory import Factory
from src.worker import Worker

def create_factory(conveyor_length, factory_products):
    workers = [[Worker(), Worker()] for _ in range(conveyor_length)]
    return Factory(conveyor_length, factory_products, workers)

def test_create_factory():
    conveyor_length = 5
    factory_products = ["a"]

    factory = create_factory(conveyor_length, factory_products)

    assert len(factory.conveyor_belt) == conveyor_length
    assert list(factory.conveyor_belt) == [None for _ in range(conveyor_length)]

def test_add_item_to_conveyor():
    conveyor_length = 5
    factory_products = ["a"]

    factory = create_factory(conveyor_length, factory_products)

    factory.add_item_to_conveyor()

    assert (list(factory.conveyor_belt) == [None, None, None, None, "a"] or list(factory.conveyor_belt) == [None, None, None, None, None])
    assert factory.retults == [None]

def test_assign_process_return_work():
    conveyor_length = 5
    factory_products = ["a"]

    factory = create_factory(conveyor_length, factory_products)

    factory.conveyor_belt = deque(["a", "a", "a", "a", "a"], 5)

    factory.worker_item_pick()

    assert list(factory.conveyor_belt) == [None, None, None, None, None]

    factory.workers_do_work()
    factory.workers_do_work()
    factory.workers_do_work()
    factory.workers_do_work()

    factory.conveyor_belt = deque([None, None, None, None, None], 5)

    factory.worker_item_pick()

    assert set(factory.conveyor_belt) & set([("completed", "a"), ("completed", "a"), ("completed", "a"), ("completed", "a"), ("completed", "a")]) == set()


def test_only_one_worker_pick_at_one_time():
    conveyor_length = 5
    factory_products = ["a"]

    factory = create_factory(conveyor_length, factory_products)

    factory.conveyor_belt = deque(["a", "a", "a", "a", "a"], 5)

    factory.worker_item_pick()

    worker_status = [[w.available for w in p] for p in factory.workers]

    assert all(any(x) for x in worker_status)

def test_only_one_worker_return_at_a_time():
    conveyor_length = 5
    factory_products = ["a"]

    factory = create_factory(conveyor_length, factory_products)

    factory.conveyor_belt = deque(["a", "a", "a", "a", "a"], 5)

    factory.worker_item_pick()

    factory.conveyor_belt = deque(["a", "a", "a", "a", "a"], 5)

    factory.worker_item_pick()

    factory.workers_do_work()
    factory.workers_do_work()
    factory.workers_do_work()
    factory.workers_do_work()

    factory.conveyor_belt = deque([None, None, None, None, None], 5)

    factory.worker_item_pick()

    worker_status = [[w.available for w in p] for p in factory.workers]

    assert all(any(x) for x in worker_status)

def test_ony_one_worker_interacts_with_conveyor_per_process_step():
    conveyor_length = 5
    factory_products = ["a"]

    factory = create_factory(conveyor_length, factory_products)

    factory.conveyor_belt = deque([None, None, None, None, "a"], 5)

    factory.workers_do_work()
    factory.workers_do_work()
    factory.workers_do_work()
    factory.workers_do_work()

    factory.conveyor_belt = deque([None, None, None, None, "a"], 5)

    factory.worker_item_pick()

    assert list(factory.conveyor_belt)[4] == None
