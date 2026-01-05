from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    created_at: date = Field(default_factory=date.today)


class Checkin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habit.id")
    day: date = Field(default_factory=date.today, index=True)


class HabitCreate(SQLModel):
    name: str


class CheckinCreate(SQLModel):
    day: Optional[date] = None


class HabitStats(SQLModel):
    habit_id: int
    name: str
    total_checkins: int
    current_streak: int
    checked_in_today: bool
