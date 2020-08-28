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

To run a dialog, use:

```bash
./run wikipedia_example.json
```

or more generally `./run <FILE>` where `<FILE>` is a valid JSON configuration file placed in the directory `resources/dialog`.

To see a visual graph representation of the dialog tree, use:

```bash
./inspect wikipedia_example.json
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