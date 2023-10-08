# Krita-layer-finder

A docker to find layers that colorizes a part of or the full selection.

## Installation

1. Clone this project
2. Copy [`layerfinder.desktop`](layerfinder.desktop), the [`actions`](actions/) directory, and the [`layerfinder/`](layerfinder/) directory into the `pykrita` directory in your Krita resource folder. See [the document](https://docs.krita.org/en/reference_manual/resource_management.html#resource-management) for its location.

## Usage

1. Make a selection.
2. Click Tools > Scripts > Find layers colorizing the selection.
3. The layers that colorize the selection will be labeled as blue.

## License

All files in this repository are licensed under GNU General Public License v3.0. See [LICENSE](LICENSE).
