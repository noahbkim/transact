import abc
from typing import Any, Callable, List, Optional

StepFunctor = Callable[[Any], Any]
StepFunctorList = List[Optional[StepFunctor]]


class Step(abc.ABC):
    """Requires do and undo."""

    @staticmethod
    def do(state: Any) -> bool:
        """Execute the step."""

    @staticmethod
    def undo(state: Any) -> bool:
        """Undo the step assuming it's been done."""


class Setup(abc.ABC):
    """Setup step."""

    @staticmethod
    def setup(state: Any) -> bool:
        """Always run prior to execution for both direction."""


class Transaction:
    """Core transaction methods."""

    @classmethod
    def _execute(
            cls,
            setup_steps: StepFunctorList,
            do_steps: StepFunctorList,
            undo_steps: StepFunctorList,
            state: Any) -> bool:
        """Run the transaction."""

        for setup in setup_steps:
            result = setup(state)
            if not result:
                return False

        for i, do in enumerate(do_steps):
            if do is None:
                continue
            result = do(state)

            # Rollback and return
            if not result:
                for undo in reversed(undo_steps[:i]):
                    if undo is None:
                        continue
                    result = undo(state)
                    if not result:
                        raise RuntimeError("transaction reached invalid state")
                return False

        return True

    @classmethod
    def _steps(cls) -> List[Step]:
        """Relies on dictionary ordering."""

        for value in cls.__dict__.values():
            if isinstance(value, type) and issubclass(value, Step):
                yield value

    @classmethod
    def _setups(cls) -> List[Setup]:
        """Relies on dictionary ordering."""

        for value in cls.__dict__.values():
            if isinstance(value, type) and issubclass(value, Setup):
                yield value

    @classmethod
    def do(cls, state: Any) -> bool:
        """Execute forward."""

        _steps = list(cls._steps())
        setup_steps = [s.setup for s in cls._setups()]
        do_steps = [s.do for s in _steps]
        undo_steps = [s.undo for s in _steps]
        return cls._execute(setup_steps, do_steps, undo_steps, state)

    @classmethod
    def undo(cls, state: Any) -> bool:
        """Execute backward."""

        _steps = list(cls._steps())
        _steps.reverse()
        setup_steps = [s.setup for s in cls._setups()]
        do_steps = [s.undo for s in _steps]
        undo_steps = [s.do for s in _steps]
        return cls._execute(setup_steps, do_steps, undo_steps, state)


class StateLogging:
    """Logging mixin."""

    log: List[str]

    def __init__(self):
        """Initialize log."""

        super().__init__()
        self.log = []

    def print(self, *args, end="\n", sep=" "):
        """Write to the log."""

        self.log.append(sep.join(args) + end)
