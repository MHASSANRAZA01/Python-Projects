import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Todo App",
    page_icon="✅",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1rem;
    }
    .task-container {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 5px solid #4CAF50;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: black;
    }
    .delete-btn {
        color: white;
        background-color: #FF5252;
        padding: 5px 10px;
        border-radius: 5px;
        text-decoration: none;
        font-size: 0.8rem;
    }
    .add-btn {
        background-color: #4CAF50;
        color: black;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 4px;
        cursor: pointer;
    }
    .exit-btn {
        background-color: #9E9E9E;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 4px;
        cursor: pointer;
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
        color: black;
    }
    
    /* Improved button styles */
    div.stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Main app header
st.markdown("<div class='main-header'>✅ Todo List App</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Manage your tasks efficiently</div>", unsafe_allow_html=True)

# Add Task Section
st.markdown("## 📌 Add Task")
new_task = st.text_input("Enter a new task:", placeholder="Type your task here...")

if st.button("Add Task", key="add", help="Click to add a new task"):
    if new_task:
        st.session_state.tasks.append(new_task)
        st.success(f"Task '{new_task}' added successfully!")
    else:
        st.error("Task cannot be empty!")

# Show Tasks Section
st.markdown("## 📋 Your Tasks")

if not st.session_state.tasks:
    st.info("You don't have any tasks yet. Add some tasks to get started!")
else:
    for i, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"<div class='task-container'>{task}</div>", unsafe_allow_html=True)
        with col2:
            if st.button("Delete", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                st.success("Task deleted successfully!")
                st.rerun()

# Exit Button
st.markdown("## 🚪 Exit")
st.markdown("Click below to exit the application.")

if st.button("Exit Application", key="exit"):
    st.markdown("Goodbye! The application will close when you refresh or navigate away.")
    st.snow()
    st.stop()

# Footer
st.markdown("---")
st.markdown("### Create By Hassan Raza")
