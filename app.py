import streamlit as st
from datetime import datetime, date

# ── Initialize storage ───────────────────────────────
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.title("🕒 Simple Time Management App")

# ── Add a new task ───────────────────────────────────
with st.form("add_task_form"):
    desc      = st.text_input("Task Description")
    due_date  = st.date_input("Due Date", date.today())
    due_time  = st.time_input("Due Time", datetime.now().time().replace(second=0, microsecond=0))
    submitted = st.form_submit_button("➕ Add Task")

    if submitted:
        if not desc:
            st.warning("Please enter a task description.")
        else:
            due_dt = datetime.combine(due_date, due_time)
            st.session_state.tasks.append({
                "description": desc,
                "due_datetime": due_dt,
                "completed": False
            })
            st.success(f"Added task: **{desc}**")

# ── Display & manage tasks ──────────────────────────
if st.session_state.tasks:
    st.header("📋 Your Tasks")

    # Sync each task's completed flag from its checkbox state
    for idx, task in enumerate(st.session_state.tasks):
        ck = f"completed_{idx}"
        if ck in st.session_state:
            task["completed"] = st.session_state[ck]

    # Render each task in its own row
    for idx, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([4,1,1])
        
        # Task info & countdown
        with col1:
            text = task["description"]
            if task["completed"]:
                text = f"~~{text}~~"
            st.write(text)
            st.write(task["due_datetime"].strftime("%Y-%m-%d %H:%M"))
            if not task["completed"]:
                delta = task["due_datetime"] - datetime.now()
                timer = str(delta).split('.')[0]
                st.write(timer if delta.total_seconds()>0 else "⚠️ Overdue!")
        
        # Completed checkbox
        with col2:
            st.checkbox("Done", key=f"completed_{idx}", value=task["completed"])
        
        # Delete button
        with col3:
            if st.button("🗑️ Delete", key=f"delete_{idx}"):
                st.session_state.tasks.pop(idx)
                st.experimental_rerun()
else:
    st.info("No tasks yet. Add one above!")
