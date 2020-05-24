from typing import Any, Dict, Callable, List, Optional
from dataclasses import dataclass

Step = Callable[[Any], Any]
StepList = List[Optional[Step]]


@dataclass(eq=False)
class Steps:
    """Registrar and executor."""

    _steps: StepList
    _opposite_steps: StepList
    _index: Dict[str, int]
    _reverse: bool

    def register(self, name: str) -> Callable[[Step], Step]:
        """Register a step."""

        def register(step: Step):
            index = self._index.get(name)
            if index is None:
                self._index[name] = len(self._steps)
                self._steps.append(step)
                self._opposite_steps.append(None)
            else:
                self._steps[index] = step
            return step

        return register

    def __call__(self, state: Any) -> bool:
        """Execute with step lists."""

        _steps = self._steps
        _opposite_steps = self._opposite_steps
        if self._reverse:
            _steps = _steps[::-1]
            _opposite_steps = _opposite_steps[::-1]

        for i, do in enumerate(_steps):
            if do is None:
                continue
            result = do(state)

            # Rollback and return
            if not result:
                for undo in reversed(_opposite_steps[:i]):
                    if undo is None:
                        continue
                    result = undo(state)
                    if not result:
                        raise RuntimeError("transaction reached invalid state")
                return False

        return True


class Transaction:
    """Core transaction methods."""

    do: Steps
    undo: Steps

    def __init__(self):
        """Setup defaults."""

        _do = []
        _undo = []
        _index = {}
        self.do = Steps(_do, _undo, _index, _reverse=False)
        self.undo = Steps(_undo, _do, _index, _reverse=True)
