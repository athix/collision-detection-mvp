# Collision detection MVP

Minimal codebase to visualize and simulate continuous collision detection.

## Requirements

* Python3
* Pip3
* PyYAML - `pip3 install pyyaml`
* Panda3D - `pip3 install panda3d`

## Usage

To run the client:

1) `cd ./aeonsplice/`
2) `python3 client.py`

The client currently accepts `.yaml` files with appropriate formatting. There is
currently little-to-no input validation, as this is just a quick and dirty
proof-of-concept.

## TODO

- [X] ~Pick a visualizer & language~ **(Python w/ Panda3D)**
- [X] ~Data format to store object meta and positional information.~ **(YAML)**
- [X] ~Visualizer for data format.~
- [ ] Turn input
- [ ] Turn processing (simple input/direct 3d translations, no collision)
- [ ] Collision functions
  - [ ] Fast path overlap detection (render paths and max radius of objects as 3d objects, check for overlap)
  - [ ] Precise path overlap/fast collision detection (Same as above, but as a function of time, skip above if performant enough)
  - [ ] Precise collision detection (exact object collision detection)
- [ ] Turn processing (with collision detection)
- [ ] Multiple scenes to test various collision scenarios.
  - [ ] 2 body head-on collision
  - [ ] 3d game of pool (multiple indirect collisions, no gravity)
  - [ ] 2d game of pool (gravity + immovable table)
