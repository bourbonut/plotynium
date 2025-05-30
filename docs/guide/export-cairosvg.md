# Export with cairosvg

[`cairosvg`](https://cairosvg.org/) is a command-line interface for converting SVG to PNG, PDF, PS.

## Installation

```bash
pip install cairosvg
```

Check the [official website](https://cairosvg.org/) for more information.

## Usage

```console
$ cairosvg --help
usage: cairosvg [-h] [-v] [-f {eps,pdf,png,ps,svg}] [-d DPI] [-W WIDTH] [-H HEIGHT] [-s SCALE] [-b COLOR] [-n] [-i] [-u] [--output-width OUTPUT_WIDTH] [--output-height OUTPUT_HEIGHT] [-o OUTPUT] input

Convert SVG files to other formats

positional arguments:
  input                 input filename or URL

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f {eps,pdf,png,ps,svg}, --format {eps,pdf,png,ps,svg}
                        output format
  -d DPI, --dpi DPI     ratio between 1 inch and 1 pixel
  -W WIDTH, --width WIDTH
                        width of the parent container in pixels
  -H HEIGHT, --height HEIGHT
                        height of the parent container in pixels
  -s SCALE, --scale SCALE
                        output scaling factor
  -b COLOR, --background COLOR
                        output background color
  -n, --negate-colors   replace every vector color with its complement
  -i, --invert-images   replace every raster pixel with its complementary color
  -u, --unsafe          resolve XML entities and allow very large files (WARNING: vulnerable to XXE attacks and various DoS)
  --output-width OUTPUT_WIDTH
                        desired output width in pixels
  --output-height OUTPUT_HEIGHT
                        desired output height in pixels
  -o OUTPUT, --output OUTPUT
                        output filename
```

For instance, after running the example `examples/pca.py`, you can convert the SVG to PNG with `cairosvg`:

```bash
python examples/pca.py && cairosvg pca.svg -o pca.png
```
