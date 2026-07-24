import enum
from typing import Callable, Any

class State(enum.Enum):
    PLAN = "plan"
    CONFIRM = "confirm"
    EXECUTE = "execute"
    REFLECT = "reflect"
    ROLLBACK = "rollback"
    COMPLETE = "complete"

class StateMachine:
    def __init__(self):
        self.state = State.PLAN
        self.plan_steps = []  # type: list[Callable[[], Any]]
        self.results = []

    def set_plan(self, steps):
        self.plan_steps = steps
        self.state = State.CONFIRM

    def confirm_and_execute(self):
        if self.state != State.CONFIRM:
            raise RuntimeError("State machine not in CONFIRM state")
        resp = input("Proceed with the plan? (y/n): ").strip().lower()
        if resp != 'y':
            self.state = State.ROLLBACK
            return
        self.state = State.EXECUTE
        for step in self.plan_steps:
            try:
                result = step()
                self.results.append(result)
            except Exception as e:
                print(f"Error during step: {e}")
                self.state = State.ROLLBACK
                return
        self.state = State.REFLECT

    def reflect(self):
        if self.state != State.REFLECT:
            raise RuntimeError("State machine not in REFLECT state")
        # Simple reflection: just print results
        for i, res in enumerate(self.results, 1):
            print(f"Step {i} result: {res}")
        self.state = State.COMPLETE

    def rollback(self):
        if self.state != State.ROLLBACK:
            raise RuntimeError("State machine not in ROLLBACK state")
        # Placeholder for git rollback logic
        print("Rollback requested – implement git rollback here.")
        self.state = State.COMPLETE

    def run(self):
        if self.state == State.CONFIRM:
            self.confirm_and_execute()
        if self.state == State.REFLECT:
            self.reflect()
        if self.state == State.ROLLBACK:
            self.rollback()
        if self.state == State.COMPLETE:
            print("Workflow complete.")
