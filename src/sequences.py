"""Outreach sequence definitions for different prospect segments."""

from dataclasses import dataclass
from datetime import datetime, timedelta

from config import SEGMENTS


@dataclass
class SequenceStep:
    """A single step in an outreach sequence."""

    day: int
    action: str
    description: str


@dataclass
class OutreachSequence:
    """Full outreach sequence for a prospect segment."""

    segment: str
    steps: list[SequenceStep]

    def get_next_step(self, current_day: int) -> SequenceStep | None:
        """Get the next step in the sequence based on current day."""
        for step in self.steps:
            if step.day > current_day:
                return step
        return None

    def get_send_date(self, start_date: datetime, step: SequenceStep) -> datetime:
        """Calculate the send date for a sequence step."""
        return start_date + timedelta(days=step.day)


PROFESSOR_SEQUENCE = OutreachSequence(
    segment="professor",
    steps=[
        SequenceStep(
            day=0,
            action="connection_request",
            description="Personalized request referencing their research or recent publication",
        ),
        SequenceStep(
            day=3,
            action="first_followup",
            description="Thank for connecting, mention specific paper or talk, ask about research direction",
        ),
        SequenceStep(
            day=7,
            action="value_message",
            description="Share a relevant economics paper or dataset they might find interesting",
        ),
        SequenceStep(
            day=14,
            action="guest_lecture_invite",
            description="Invite to speak at society event on their area of expertise",
        ),
    ],
)

ALUMNI_SEQUENCE = OutreachSequence(
    segment="alumni",
    steps=[
        SequenceStep(
            day=0,
            action="connection_request",
            description="Warm intro referencing shared university and economics interest",
        ),
        SequenceStep(
            day=2,
            action="first_followup",
            description="Ask about their career path from economics degree to current role",
        ),
        SequenceStep(
            day=5,
            action="mentorship_ask",
            description="Invite to join mentorship program or career panel",
        ),
        SequenceStep(
            day=10,
            action="event_invite",
            description="Invite to upcoming alumni networking event",
        ),
    ],
)

PROFESSIONAL_SEQUENCE = OutreachSequence(
    segment="professional",
    steps=[
        SequenceStep(
            day=0,
            action="connection_request",
            description="Reference their work in economics-adjacent industry",
        ),
        SequenceStep(
            day=3,
            action="first_followup",
            description="Share insight about their industry from economic perspective",
        ),
        SequenceStep(
            day=7,
            action="value_message",
            description="Share relevant report, analysis, or upcoming event",
        ),
        SequenceStep(
            day=14,
            action="soft_ask",
            description="Invite to speak at society event or suggest collaboration",
        ),
        SequenceStep(
            day=21,
            action="graceful_close",
            description="Acknowledge busy schedule, leave door open for future",
        ),
    ],
)

STUDENT_SEQUENCE = OutreachSequence(
    segment="student",
    steps=[
        SequenceStep(
            day=0,
            action="connection_request",
            description="Casual intro mentioning shared economics interest",
        ),
        SequenceStep(
            day=2,
            action="event_invite",
            description="Invite to upcoming society event or study group",
        ),
        SequenceStep(
            day=5,
            action="membership_pitch",
            description="Highlight society benefits and invite to join",
        ),
    ],
)

SEQUENCES = {
    "professor": PROFESSOR_SEQUENCE,
    "alumni": ALUMNI_SEQUENCE,
    "professional": PROFESSIONAL_SEQUENCE,
    "student": STUDENT_SEQUENCE,
}


def get_sequence(segment: str) -> OutreachSequence:
    """Get the outreach sequence for a given segment."""
    return SEQUENCES.get(segment, PROFESSIONAL_SEQUENCE)
