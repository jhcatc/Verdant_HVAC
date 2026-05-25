from typing import Literal

OpportunityStage = Literal[
    "LEAD",
    "QUALIFIED",
    "PROPOSAL",
    "NEGOTIATION",
    "WON",
    "LOST"
]

VALID_TRANSITIONS = {
    "LEAD": ["QUALIFIED", "LOST"],
    "QUALIFIED": ["PROPOSAL", "LOST"],
    "PROPOSAL": ["NEGOTIATION", "LOST"],
    "NEGOTIATION": ["WON", "LOST"],
    "WON": [],
    "LOST": []
}


def can_transition(current: str, new: str) -> bool:
    return new in VALID_TRANSITIONS.get(current, [])


def require_transition(current: str, new: str):
    if not can_transition(current, new):
        raise ValueError(
            f"Invalid stage transition: {current} → {new}"
        )