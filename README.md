# Tic-Tac-Toe CLI

Simple Python console game:

* Play against an unbeatable AI (Minimax + α-β pruning)
* No dependencies, works with Python 3.6+

## Run

```bash
python main.py
```

Enter X or O, then moves as `row,col` (0–2).

## Build .exe

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

Enjoy!
