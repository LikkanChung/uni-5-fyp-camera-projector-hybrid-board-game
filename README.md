# Camera-Projector Hybrid Board Game

This repository implements my Final Year Project, implementing a camera-projector hybrid board game model.

## Hardware Requirements:
* Projector
* USB Peripheral Camera (webcam)

## Hardware Setup:
1. Establish a playing surface. This can be something like a desk or table, 
   but the surface should have significant contrast in colour to the board.
2. The projector and camera should be mounted so that they project onto or have a bird's eye view
   of the playing surface.
3. The projector must be connected to the device on which the software is running.
   Connect and set up the projector according to the manufacturer's instructions.
   It must also be the main display, or mirror the main display. 
4. The USB camera must be connected to the device on which the software is running.
5. The projector and camera should be set up in a way which is safe and secure, without risk of falling over.

## Software Setup:

### Prerequisites:
* [Python 3](https://www.python.org/)
* [Poetry package manager](https://python-poetry.org/)

### Installation:
1. Ensure prerequisite software is installed. 
2. Ensure the current directory is the root of the project. i.e. In the same directory as this file.
3. Install the project with Poetry: `poetry install`

> **Note:** The `setup.sh` script can be used for the above steps.

### Configuration:
In order for the software to run correctly, the `config.yaml` file must be setup. 

Its path is: `src/client/config.yaml`

It has the following structure:

```yaml
debug:
  enabled: # True/False - If the debug window should be displayed
  x: # 512 - Default width of the debug window (pixels)
  y: # 288 - Default height of the debug window (pixels)
client:
  font: # 32 - Default font size for text used in game
  control:
    quit: # esc - Default key to close the game
  color:
    board_detect_threshold: # 200 - Default board vs playing surface threshold (0-255). 
                            #       Use the debug tool to check this value is suitable. 
    token_background_threshold: # 200 - Default token vs board threshold (0-255).
    classes:
      blue: # Blue colour token with default RGB values - this should not need to change
        b: 163
        g: 128
        r: 110
      red: # Red colour token with default RGB values - this should not need to change
        b: 143
        g: 128
        r: 170
  detection_smoothing_buffer: 
    board: 15 # Smoothing buffers which average coordinates - this should not need to change
    token: 50 # Smoothing buffers which average coordinates - this should not need to change
    token_calibration: 5 # Number of seconds to wait to allow token position averaging - this should not need to change
    board_manual_offset:
      x: 300 # Manual offset board position in x direction
      y: 50 # Manual offset board position in y direction
  token_update_timeout: # 15 - Default number of updates missed before token is removed
resolution:
  camera:
    id: # 0 - Default device ID of camera as found by cv2. May be (0, 1, 2, ...) If no camera detected, try adding 1
    x: 1920 # Default width dimension of camera - this should not need to change
    y: 1080 # Default height dimension of camera - this should not need to change
    scale_by: 1.5  # Default scale factor to limit board area - this may change if necessary
  projector:
    x: 1920 # Default width dimension of projector - this should be the same as your main display
    y: 1080 # Default height dimension of projector - this should be the same as your main display
```

### Usage:
1. Set up `config.yaml`
2. Run with `poetry run client`

## Prototypes

There are additional packages which document initial work on components, and are proofs of concept. 
These are found in `prototypes`, and are themselves each a Poetry project. 

The setup for each is identical to the main project, except the working directory should be the root of each prototype, 
i.e. The current directory should include the `pyproject.toml` file. 

> **Note:** If a project is already installed, then you should note if the Poetry virtual environment is 
  activated as installing another project may cause nested virtual environments.

Running prototypes may differ, as each prototype offers different run scripts. 
Refer to each prototype's README document for more details.
