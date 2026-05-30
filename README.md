# Simple Chess Game with Minimax AI

This project is a small Python chess game made for a **Principles of AI** subject.  
It keeps the implementation simple and uses the **Minimax algorithm with Alpha-Beta Pruning** for the computer player.

## Features

- Human vs AI chess game
- AI uses Minimax
- Alpha-beta pruning is used to reduce extra search
- Simple desktop GUI built with Tkinter
- Accepts moves in:
  - UCI format: `e2e4`
  - SAN format: `Nf3`

## Project Idea

The main AI idea used here is:

1. Generate all legal moves from the current board.
2. Look ahead a few moves using **Minimax**.
3. Assume:
   - White tries to maximize the score
   - Black tries to minimize the score
4. Use a simple evaluation function based on:
   - Pawn = 100
   - Knight = 320
   - Bishop = 330
   - Rook = 500
   - Queen = 900
   - small positional bonuses for better squares
5. Choose the move with the best score.

## Files

- `main.py` - game logic, AI, and GUI
- `requirements.txt` - dependency list

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## How to Play

- You play as **White**
- Click a piece and then a destination square to move it
- You can also type a move in the input box
- Examples:
  - `e2e4`
  - `Nf3`
  - `Bb5`
- Click **New Game** to restart

## Why This Is Good for an AI Subject

This project is suitable for a 2nd-year undergraduate AI submission because:

- it clearly demonstrates **state-space search**
- it uses **Minimax**, which is a standard AI algorithm
- it includes **alpha-beta pruning**, which is an optimization
- the code is short and easy to explain in a viva or report

## Limitations

- The AI is simple and not as strong as real chess engines
- The evaluation function is mostly based on material and simple positional scores
- Search depth is small to keep the program fast and understandable
- Pawn promotion in the GUI defaults to a queen

## Suggested Viva Explanation

You can explain the project like this:

"The chess board is the state. Legal moves are the actions.  
The Minimax algorithm checks future states and selects the move that gives the best result assuming the opponent also plays optimally.  
Alpha-beta pruning improves Minimax by cutting unnecessary branches."
