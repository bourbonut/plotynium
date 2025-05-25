from math import sqrt

import pytest
from plotynium.properties import (
    DEFAULT_CANVAS_WIDTH,
    DEFAULT_LEGEND_HEIGHT,
    DEFAULT_LEGEND_WIDTH,
    DEFAULT_SQUARE_SIZE,
    CanvasProperties,
    LegendProperties,
    Margin,
    Properties,
)


@pytest.fixture
def margin():
    return Margin(10, 15, 20, 25)


@pytest.fixture
def properties(margin):
    return Properties(500, 30, margin)


@pytest.fixture
def canvas_properties():
    return CanvasProperties()


@pytest.fixture
def legend_properties():
    return LegendProperties()


def test_margin(margin):
    assert margin.top == 10
    assert margin.left == 15
    assert margin.bottom == 20
    assert margin.right == 25


def test_init_properties(properties, margin):
    assert properties._width == 500
    assert properties._height == 30
    assert properties._margin.top == margin.top
    assert properties._margin.left == margin.left
    assert properties._margin.bottom == margin.bottom
    assert properties._margin.right == margin.right


def test_properties_method_property(properties, margin):
    assert properties.width == 500
    assert properties.height == 30
    assert properties.margin.top == margin.top
    assert properties.margin.left == margin.left
    assert properties.margin.bottom == margin.bottom
    assert properties.margin.right == margin.right


def test_properties_set_width(properties):
    assert properties._width == 500
    properties.set_width(29)
    assert properties._width == 29


def test_properties_set_height(properties):
    assert properties._height == 30
    properties.set_height(1223)
    assert properties._height == 1223


def test_properties_set_margin(properties, margin):
    assert properties._margin.top == margin.top
    assert properties._margin.left == margin.left
    assert properties._margin.bottom == margin.bottom
    assert properties._margin.right == margin.right
    properties.set_margin(Margin(1, 2, 3, 4))
    assert properties._margin.top == 1
    assert properties._margin.left == 2
    assert properties._margin.bottom == 3
    assert properties._margin.right == 4


def test_init_canvas_properties(canvas_properties):
    assert canvas_properties.width == DEFAULT_CANVAS_WIDTH
    assert canvas_properties.height == int(DEFAULT_CANVAS_WIDTH / sqrt(2))
    assert canvas_properties.margin.top == 0
    assert canvas_properties.margin.left == 0
    assert canvas_properties.margin.bottom == 0
    assert canvas_properties.margin.right == 0
    assert canvas_properties._translate_x == 0
    assert canvas_properties._translate_y == 0


def test_canvas_properties_set_translate(canvas_properties):
    assert canvas_properties._translate_x == 0
    assert canvas_properties._translate_y == 0
    canvas_properties.set_translate(10, 20)
    assert canvas_properties._translate_x == 10
    assert canvas_properties._translate_y == 20


def test_canvas_properties_translate_property(canvas_properties):
    assert canvas_properties._translate_x == 0
    assert canvas_properties._translate_y == 0
    assert canvas_properties.translate is None
    canvas_properties.set_translate(10, 0)
    assert isinstance(canvas_properties.translate, str)
    assert canvas_properties.translate == "translate(10, 0)"
    canvas_properties.set_translate(0, 9)
    assert isinstance(canvas_properties.translate, str)
    assert canvas_properties.translate == "translate(0, 9)"


def test_init_legend_properties(legend_properties):
    assert legend_properties.width == DEFAULT_LEGEND_WIDTH
    assert legend_properties.height == DEFAULT_LEGEND_HEIGHT
    assert (
        legend_properties.margin.top
        == (DEFAULT_LEGEND_HEIGHT - DEFAULT_SQUARE_SIZE // 2) // 2
    )
    assert legend_properties.margin.left == DEFAULT_SQUARE_SIZE
    assert (
        legend_properties.margin.bottom
        == (DEFAULT_LEGEND_HEIGHT - DEFAULT_SQUARE_SIZE // 2) // 2
    )
    assert legend_properties.margin.right == DEFAULT_SQUARE_SIZE


def test_legend_properties_classmethod():
    legend_properties = LegendProperties.new(1, 2, 3, 4, 5, 6)
    assert isinstance(legend_properties, LegendProperties)
    assert legend_properties.width == 1
    assert legend_properties.height == 2
    assert legend_properties.margin.top == 3
    assert legend_properties.margin.left == 4
    assert legend_properties.margin.bottom == 5
    assert legend_properties.margin.right == 6
