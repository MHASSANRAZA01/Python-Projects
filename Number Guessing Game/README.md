# Number Guessing Game

A fun, interactive number guessing game built with Streamlit. The game generates a random number and lets the user guess it, providing feedback after each attempt.

## Features

- Beautiful, modern UI
- Multiple difficulty levels
- Custom number range setting
- Visual feedback for each guess
- Attempt counter
- Celebratory animations on winning

## Requirements

- Python 3.7 or higher
- Streamlit
- Pandas (for future enhancements)

## Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## How to Run

Run the following command in your terminal:

```bash
streamlit run main.py
```

This will start a local Streamlit server and open the game in your default web browser.

## How to Play

1. The computer will generate a random number within the specified range (default: 1-100).
2. Your goal is to guess this number in as few attempts as possible.
3. After each guess, you'll receive a hint: "Too high" or "Too low".
4. Keep guessing until you find the correct number or run out of attempts.
5. You can reset the game at any time or change the difficulty/range in the settings.

## Game Modes

- **Easy**: 10 attempts
- **Medium**: 7 attempts
- **Hard**: 5 attempts
- **Unlimited**: No limit on attempts

## Customization

You can customize the game by:

- Setting a custom number range
- Selecting different difficulty levels

Enjoy the game! 🎮
