import streamlit as st
import calendar
from datetime import datetime

def remove_holidays(working_days, holidays):
    updated_working_days = [
        day for day in working_days if day not in holidays
    ]
    
    return updated_working_days
    
def get_working_days(year, month, holidays=None):

    if holidays is None:
        holidays = []

    total_days = calendar.monthrange(year, month)[1]

    working_days = []
    non_working_days = []

    for day in range(1, total_days + 1):

        current_date = datetime(year, month, day)

        weekday = current_date.weekday()

        # date_str = current_date.strftime("%Y-%m-%d")
        date_str = f"{day:02d}-{month:02d}-{year}"
        date_str_date = date_str[:2]

        # Exclude Saturday & Sunday
        if weekday not in (5, 6):
            working_days.append(int(date_str_date))
        else:
            non_working_days.append(int(date_str_date))  
            
    updated_working_day = remove_holidays(working_days, holidays)    

    return working_days, non_working_days, updated_working_day


def office_requirement_status(
        required_office_days,
        office_days,
        leave_days):

    completed = office_days + leave_days

    remaining = required_office_days - completed

    if remaining < 0:
        remaining = 0

    return completed, remaining

def calculate_office_req(
    total_working_days,
    office_days_done,
    wfh_days,
    leave_days,
    mandatory_office_days,
    holidays_len
):
    completed_office_days = office_days_done + leave_days
    remaining_office_days = total_working_days - completed_office_days - wfh_days
    remaining_office_days_to_go = mandatory_office_days - completed_office_days
    
    
    return {
        "Working Days" : total_working_days + holidays_len,
        "Holidays" : holidays_len,
        "Working days to attend office" : total_working_days,
        "In - Office Days Done": office_days_done,
        "WFH Days": wfh_days,
        "Leave Days": leave_days,
        "Total Days completed for Office": completed_office_days + wfh_days,
        "Remaining office days": remaining_office_days,
        "Mandatory Office Days": mandatory_office_days,
        "In-Office Days Completed" : completed_office_days,
        "Remaining In-Office Days to go": remaining_office_days_to_go
    }


# --------------------------------

st.title("Office Attendance Tracker")

today = datetime.today()

# year = today.year
year = st.number_input(
    "Year",
    value=today.year
)
# month = today.month
month = st.number_input(
    "Month",
    min_value=1,
    max_value=12,
    value=today.month
)

mandatory_office_days = st.number_input(
    "Mandatory Office Days",
    value = 16
)



office_days_done = st.number_input(
    "Office Days Done",
    value = 0
)

wfh_days = st.number_input(
    "WFH Days",
    value = 0
)


leave_days = st.number_input(
    "Leave Days",
    value = 0
)

holidays_input = st.text_input(
    "Holidays (comma seperated)",
    "1"
)

holidays = [
    int(day.strip())
    for day in holidays_input.split(",")
    if day.strip()
]


if st.button("Calculate"):

    working_days, non_working_days, updated_working_days = get_working_days(
        year,
        month,
        holidays
    )
    
    # st.subheader("Working days")
    # st.write(updated_working_days)
    
    # st.subheader("Weekdays days")
    # st.write(non_working_days)
    
    result = calculate_office_req(
        total_working_days=len(updated_working_days),
        office_days_done=office_days_done,
        wfh_days=wfh_days,
        leave_days=leave_days,
        mandatory_office_days=mandatory_office_days,
        holidays_len=len(holidays)
    )
    
    st.subheader("Summary")
    
    for key, value in result.items():
        if key not in ["Remaining office days", "Remaining office Days to go"]:
            st.success(f"{key}  -> {value}")
        else:
            st.warning(f"{key}  -> {value}")
            
        
#   return {
#         "Total working Days" : total_working_days,
#         "Office Days Done": office_days_done,
#         "WFH Days": wfh_days,
#         "Leave Days": leave_days,
#         "Total Days completed for office": completed_office_days + wfh_days,
#         "Remaining office days": remaining_office_days,
#         "Mandatory Office Days": mandatory_office_days,
#         "Office Days Counted" : completed_office_days,
#         "Remaining office Days to go": remaining_office_days_to_go
#     }
    
    
    # st.success(f"Completed Office Count: {completed}")
    # st.warning(f"Remaining Office Days Needed: {remaining}")

# working_days = get_working_days(year, month) 

# st.write("Total Working Days:", len(working_days))

# office_days = st.number_input(
#     "Office Days",
#     min_value=0,
#     step=1
# )

# wfh_days = st.number_input(
#     "WFH Days",
#     min_value=0,
#     step=1
# )

# leave_days = st.number_input(
#     "Leave Days",
#     min_value=0,
#     step=1
# )

# required_office_days = 16

# if st.button("Calculate"):

#     completed, remaining = office_requirement_status(
#         required_office_days,
#         office_days,
#         leave_days
#     )

#     st.success(f"Completed Office Count: {completed}")
#     st.warning(f"Remaining Office Days Needed: {remaining}")
