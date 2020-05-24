from transact import Transaction

from dataclasses import dataclass


@dataclass
class State:
    value: int
    fail: bool


t = Transaction()


@t.do.register("s1")
def do_step1(s: State):
    s.value += 2
    return True


@t.undo.register("s1")
def undo_step1(s: State):
    s.value -= 2
    return True


@t.do.register("s2")
def do_step2(s: State):
    if s.fail:
        return False

    s.value *= 3
    return True


@t.undo.register("s2")
def undo_step2(s: State):
    s.value /= 3
    return True


@t.do.register("s3")
def do_step3(s: State):
    s.value += 5
    return True


@t.undo.register("s3")
def undo_step3(s: State):
    s.value -= 5
    return True


s = State(value=1, fail=False)
t.do(s)
print(s)

s = State(value=1, fail=True)
t.do(s)
print(s)

s = State(value=14, fail=False)
t.undo(s)
print(s)
