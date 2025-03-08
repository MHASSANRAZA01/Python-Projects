import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="Number Guessing Game",
    page_icon="🎮",
    layout="centered",
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #26A69A;
        margin-bottom: 1rem;
    }
    .success-text {
        color: #66BB6A;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .failure-text {
        color: #EF5350;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .hint-text {
        color: #7E57C2;
        font-style: italic;
        font-size: 1.1rem;
    }
    .attempt-counter {
        font-weight: bold;
        font-size: 1.1rem;
        color: #FF9800;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
    }
    .difficulty-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'random_number' not in st.session_state:
    st.session_state.random_number = random.randint(1, 100)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'max_attempts' not in st.session_state:
    st.session_state.max_attempts = 0  # 0 means unlimited attempts
if 'min_range' not in st.session_state:
    st.session_state.min_range = 1
if 'max_range' not in st.session_state:
    st.session_state.max_range = 100
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'win' not in st.session_state:
    st.session_state.win = False

# Function to reset the game
def reset_game():
    st.session_state.random_number = random.randint(
        st.session_state.min_range, st.session_state.max_range
    )
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.feedback = ""
    st.session_state.win = False

# Function to set difficulty
def set_difficulty(difficulty):
    if difficulty == "Easy":
        st.session_state.max_attempts = 10
    elif difficulty == "Medium":
        st.session_state.max_attempts = 7
    elif difficulty == "Hard":
        st.session_state.max_attempts = 5
    elif difficulty == "Unlimited":
        st.session_state.max_attempts = 0
    reset_game()

# Function to handle guess submission
def check_guess():
    # Get user guess
    try:
        guess = int(st.session_state.user_guess)
        st.session_state.attempts += 1
        
        # Check if guess is correct
        if guess == st.session_state.random_number:
            st.session_state.win = True
            st.session_state.game_over = True
            st.session_state.feedback = f"🎉 Congratulations! You guessed the number {guess} correctly!"
        elif guess < st.session_state.random_number:
            st.session_state.feedback = "📈 Too low! Try a higher number."
        else:
            st.session_state.feedback = "📉 Too high! Try a lower number."
        
        # Check if maximum attempts reached
        if st.session_state.max_attempts > 0 and st.session_state.attempts >= st.session_state.max_attempts and not st.session_state.win:
            st.session_state.game_over = True
            st.session_state.feedback = f"😟 Game Over! You've used all {st.session_state.max_attempts} attempts. The number was {st.session_state.random_number}."
    
    except ValueError:
        st.session_state.feedback = "⚠️ Please enter a valid number!"

# Function to update range
def update_range():
    min_val = st.session_state.min_range_input
    max_val = st.session_state.max_range_input
    
    if min_val >= max_val:
        st.session_state.range_error = "Minimum value must be less than maximum value!"
        return
    
    st.session_state.min_range = min_val
    st.session_state.max_range = max_val
    st.session_state.range_error = ""
    reset_game()

# Main header
st.markdown("<h1 class='main-header'>🎮 Number Guessing Game</h1>", unsafe_allow_html=True)

# Game settings section
with st.expander("Game Settings", expanded=False):
    st.markdown("<h3 class='sub-header'>Difficulty Level</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Easy (10 attempts)"):
            set_difficulty("Easy")
    with col2:
        if st.button("Medium (7 attempts)"):
            set_difficulty("Medium")
    with col3:
        if st.button("Hard (5 attempts)"):
            set_difficulty("Hard")
    with col4:
        if st.button("Unlimited"):
            set_difficulty("Unlimited")
    
    st.markdown("<h3 class='sub-header'>Custom Range</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Minimum", value=st.session_state.min_range, key="min_range_input")
    with col2:
        st.number_input("Maximum", value=st.session_state.max_range, key="max_range_input")
    
    if st.button("Update Range"):
        update_range()
    
    if 'range_error' in st.session_state and st.session_state.range_error:
        st.error(st.session_state.range_error)

# Game info
st.markdown(f"""
<div style='background-color: rgba(30, 136, 229, 0.1); padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;'>
    <span style='font-weight: bold;'>Current Range:</span> {st.session_state.min_range} to {st.session_state.max_range}<br>
    <span style='font-weight: bold;'>Mode:</span> {"Unlimited attempts" if st.session_state.max_attempts == 0 else f"{st.session_state.max_attempts} attempts"}<br>
    <span class='attempt-counter'>Attempts: {st.session_state.attempts}</span>
</div>
""", unsafe_allow_html=True)

# Game interface
if not st.session_state.game_over:
    st.markdown("<h3 class='sub-header'>Guess the Number</h3>", unsafe_allow_html=True)
    
    # Input for user guess
    st.text_input(
        f"Enter your guess between {st.session_state.min_range} and {st.session_state.max_range}:",
        key="user_guess"
    )
    
    # Submit button
    if st.button("Submit Guess"):
        check_guess()
else:
    if st.session_state.win:
        st.balloons()

# Display feedback
if st.session_state.feedback:
    if "Congratulations" in st.session_state.feedback:
        st.markdown(f"<p class='success-text'>{st.session_state.feedback}</p>", unsafe_allow_html=True)
    elif "Game Over" in st.session_state.feedback:
        st.markdown(f"<p class='failure-text'>{st.session_state.feedback}</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p class='hint-text'>{st.session_state.feedback}</p>", unsafe_allow_html=True)

# Reset button
if st.button("Reset Game"):
    reset_game()

# Game instructions
with st.expander("How to Play", expanded=False):
    st.markdown("""
    1. The computer will generate a random number within the specified range.
    2. Your goal is to guess this number in as few attempts as possible.
    3. After each guess, you'll receive a hint: "Too high" or "Too low".
    4. Keep guessing until you find the correct number or run out of attempts.
    5. You can reset the game at any time or change the difficulty/range in the settings.
    
    Good luck! 🍀
    """)

# Footer
st.markdown("""
<div style='text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ccc;'>
    <p style='color: #666; font-size: 0.8rem;'>Created By Hassan Raza</p>
</div>
""", unsafe_allow_html=True)
