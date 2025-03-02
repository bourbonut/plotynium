---
hide:
    - navigation
---

# Getting started

## Requirements

Plotynium requires Python 3.10. Since Plotynium has `lxml` as its dependencies, you should check [the section about requirements for `lxml`](https://lxml.de/installation.html#requirements).

## Installation

### From PyPI

You can install Plotynium by running the following command:

```bash
pip install plotynium
```

### From source

You can install Plotynium from source if you prefer with the following command:

```bash
pip install git+https://github.com/bourbonut/plotynium
```

## Examples

You can try out examples on the Plotynium repository. First, you need to get them:

```bash
git clone --depth=1 -n --single-branch https://github.com/bourbonut/plotynium.git
cd plotynium
git sparse-checkout set --no-cone examples
cd examples
```
