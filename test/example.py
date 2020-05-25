from transact import Transaction, Step, Setup

from dataclasses import dataclass


@dataclass
class ExampleState:
    value: int
    fail: bool


class ExampleTransaction(Transaction):

    class AddOne(Step):

        @staticmethod
        def do(state: ExampleState) -> bool:
            s.value += 1
            return True

        @staticmethod
        def undo(state: ExampleState) -> bool:
            s.value -= 1
            return True

    class MultiplyThree(Step):

        @staticmethod
        def do(state: ExampleState) -> bool:
            state.value *= 3
            return True

        @staticmethod
        def undo(state: ExampleState) -> bool:
            state.value /= 3
            return True

    class AddFive(Step):

        @staticmethod
        def do(state: ExampleState) -> bool:
            state.value += 5
            return True

        @staticmethod
        def undo(state: ExampleState) -> bool:
            state.value -= 5
            return True


s = ExampleState(value=1, fail=False)
ExampleTransaction.do(s)
print(s)

s = ExampleState(value=1, fail=True)
ExampleTransaction.do(s)
print(s)

s = ExampleState(value=11, fail=False)
ExampleTransaction.undo(s)
print(s)
