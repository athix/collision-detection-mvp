# Collision detection MVP

Minimal codebase to visualize and simulate continuous collision detection.

**This code has been deprecated in favor of HTML5 using BabylonJS, VueJS, and Ruby on Rails.**

## Screenshots

![Screenshot of the Main Menu](README-main_menu.png?raw=true "Main Menu")

![Screenshot of the game interface with an entity selected](README-head_on.png?raw=true "Entity selection")

![Screenshot of alternate game loaded from a different yaml file](README-alt_head_on.png?raw=true "Alternate game file")

## Requirements

* Python3
* Pip3

## Installation

`pip3 install -r requirements.txt`

## Usage

To run the client:

1) `cd ./aeonsplice/`
2) `python3 client.py`

The client currently accepts `.yaml` files with appropriate formatting. There is
currently little-to-no input validation, as this is just a quick and dirty
proof-of-concept.
