from transact import Transaction, Step, Setup

from dataclasses import dataclass


@dataclass
class ExampleState:
    value: int
    fail: bool
    extra: bool = False


class ExampleTransaction(Transaction):

    class SetExtra(Setup):
        @staticmethod
        def setup(state: ExampleState) -> bool:
            print("setup")
            state.extra = True
            return True

    class AddOne(Step):

        @staticmethod
        def do(state: ExampleState) -> bool:
            print("add one")
            s.value += 1
            return True

        @staticmethod
        def undo(state: ExampleState) -> bool:
            print("undo add one")
            s.value -= 1
            return True

    class MultiplyThree(Step):

        @staticmethod
        def do(state: ExampleState) -> bool:
            print("multiply three")
            state.value *= 3
            return True

        @staticmethod
        def undo(state: ExampleState) -> bool:
            print("undo multiply three")
            state.value /= 3
            return True

    class AddFive(Step):

        @staticmethod
        def do(state: ExampleState) -> bool:
            if state.fail:
                return False
            print("add five")
            state.value += 5
            return True

        @staticmethod
        def undo(state: ExampleState) -> bool:
            print("undo add five")
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
