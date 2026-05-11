import streamlit as st
import calendar
from datetime import datetime


def get_working_days(year, month, holidays=None):

    if holidays is None:
        holidays = []

    total_days = calendar.monthrange(year, month)[1]

    working_days = []

    for day in range(1, total_days + 1):

        current_date = datetime(year, month, day)

        weekday = current_date.weekday()

        date_str = current_date.strftime("%Y-%m-%d")

        # Exclude Saturday & Sunday
        if weekday not in (5, 6):

            # Exclude holidays
            if date_str not in holidays:
                working_days.append(date_str)

    return working_days


def office_requirement_status(
        required_office_days,
        office_days,
        leave_days):

    completed = office_days + leave_days

    remaining = required_office_days - completed

    if remaining < 0:
        remaining = 0

    return completed, remaining


# --------------------------------

st.title("Office Attendance Tracker")

today = datetime.today()

year = today.year
month = today.month

working_days = get_working_days(year, month)

st.write("Total Working Days:", len(working_days))

office_days = st.number_input(
    "Office Days",
    min_value=0,
    step=1
)

wfh_days = st.number_input(
    "WFH Days",
    min_value=0,
    step=1
)

leave_days = st.number_input(
    "Leave Days",
    min_value=0,
    step=1
)

required_office_days = 16

if st.button("Calculate"):

    completed, remaining = office_requirement_status(
        required_office_days,
        office_days,
        leave_days
    )

    st.success(f"Completed Office Count: {completed}")
    st.warning(f"Remaining Office Days Needed: {remaining}")
