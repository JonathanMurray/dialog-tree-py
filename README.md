# Dialog Tree

A lightweight library/tool for building dialog trees and visual novels with Pygame.

<p align="middle">
    <img src="https://github.com/JonathanMurray/dialog-tree-py/blob/master/screenshots/screenshot_wikipedia_json.png" width="32%" />
    <img src="https://github.com/JonathanMurray/dialog-tree-py/blob/master/screenshots/screenshot_dragonball.png" width="32%" />
    <img src="https://github.com/JonathanMurray/dialog-tree-py/blob/master/screenshots/screenshot_wikipedia_example.png" width="32%" />
</p>

Create your own dialog experience with custom images, text and graph structure, using a simple
JSON configuration file. By using different JSON schemas you can either generate a simple sequence
of images (like a slideshow or non-interactive visual novel, if you will), or take full control over
the configuration and define exactly how the dialog nodes are connected to each other.

Note that this project is still early in development and may be missing features that seem like
no-brainers. Contributions are welcome and encouraged!

## Installation

(This project assumes that you are using Python3.) 

Install required dependencies with:

```bash
pip3 install -r requirements.txt
```

## Usage

Dialog-Tree is both a library and a tool. Check out the examples for getting a sense of how it can
be used.

These examples demonstrate how to use the provided dialog-runner by supplying it with your own
configuration and resources
```bash
# Animated dialog based on JSON configuration, using custom sound/image resources
examples/animated_dialog/run.sh

# Simple slideshow based on JSON configuration, using custom image resources
examples/slideshow/run.sh
```

These examples demonstrate how to use Dialog-Tree as a Python library in your own code-base
```bash
# An example Pygame app that sets up a dialog surface along with other content on the screen
python3 examples/custom_app

# A text-based adventure game that uses the graph parts of the library but none of the UI parts
python3 examples/text_adventure_game
``` 

To see a visual graph representation of a dialog configuration file, use:

```bash
./inspect.sh examples/animated_dialog/wikipedia.json
# This requires you to have graphviz installed on your machine
```


## Development

To run all tests, use:

```bash
./test.sh
```

### Contributing

Pull requests (and feature requests) are welcome and encouraged!

Please make sure to update tests as appropriate.

If adding image resources to repository, try to keep them small to reduce the byte size.

## License
[MIT](LICENSE.txt)