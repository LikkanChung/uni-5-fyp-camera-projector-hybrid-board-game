# Prototype: Playing Surface Board Detection

This prototype is a proof-of-concept of detecting a board using QR codes in the corners of a board.

## Setup
The setup is the same as the main project. See the main [README.md](../../README.md).
This prototype requires only a camera, and not a projector.

## Scripts
The available scripts are run using:

| Script   | Command                 |
|----------|-------------------------|
| generate | `poetry run generate`   |
| test     | `poetry run pytest`     |

### Generate
This generates some QR codes with JSON data in the main function of `src/generate.py`
Generated images are found in `tests/assets`. The composite image is used in the tests.

### Test
This script finds the QR codes and draws bounds. It follows 4 stages:
1. It loads the composite image from `tests/assets`
2. Press the space key to continue
3. It uses live camera feed (id=0) to draw bounds on live images
4. Press the Q key to quit'