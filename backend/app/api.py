from datetime import date, timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .db import create_db_and_tables, get_session
from .models import Checkin, CheckinCreate, Habit, HabitCreate, HabitStats

app = FastAPI(title="Habit Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.post("/habits", response_model=Habit)
def create_habit(habit: HabitCreate, session: Session = Depends(get_session)) -> Habit:
    name = habit.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Habit name cannot be empty")

    new_habit = Habit(name=name)
    session.add(new_habit)
    session.commit()
    session.refresh(new_habit)
    return new_habit


@app.get("/habits", response_model=list[Habit])
def list_habits(session: Session = Depends(get_session)) -> list[Habit]:
    habits = session.exec(select(Habit).order_by(Habit.id)).all()
    return habits


@app.post("/habits/{habit_id}/checkins", response_model=Checkin)
def create_checkin(
    habit_id: int, checkin: CheckinCreate, session: Session = Depends(get_session)
) -> Checkin:
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    checkin_day = checkin.day or date.today()

    existing = session.exec(
        select(Checkin).where(
            Checkin.habit_id == habit_id,
            Checkin.day == checkin_day,
        )
    ).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Check-in for this habit and day already exists"
        )

    new_checkin = Checkin(habit_id=habit_id, day=checkin_day)
    session.add(new_checkin)
    session.commit()
    session.refresh(new_checkin)
    return new_checkin


@app.get("/habits/{habit_id}/stats", response_model=HabitStats)
def habit_stats(habit_id: int, session: Session = Depends(get_session)) -> HabitStats:
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    checkins = session.exec(
        select(Checkin).where(Checkin.habit_id == habit_id)
    ).all()

    unique_days = sorted({c.day for c in checkins}, reverse=True)
    total_checkins = len(unique_days)

    today = date.today()
    checked_in_today = today in unique_days

    streak = 0
    expected_day = today
    for day in unique_days:
        if day == expected_day:
            streak += 1
            expected_day -= timedelta(days=1)
        elif day < expected_day:
            break

    return HabitStats(
        habit_id=habit.id,
        name=habit.name,
        total_checkins=total_checkins,
        current_streak=streak,
        checked_in_today=checked_in_today,
    )
