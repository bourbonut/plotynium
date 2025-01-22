import detroit as d3

def plot(
    style: dict | None = None,
    color: dict | None = None,
    width: int | None = None,
    height: int | float = None,
    margin: tuple[int, int, int, int] = None,
    marks: list | None = None,
):
    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
    )

    for mark in marks:
        marks(svg, width, height, margin)

    x = (
        d3.scale_linear()
        .set_domain([min(data, key=self.x), max(data, key=self.x)])
        .set_range([margin.left, width - margin.right])
        .nice()
    )

    y = (
        d3.scale_linear()
        .set_domain([min(data, key=self.y), max(data, key=self.y)])
        .set_range([height - margin.bottom, margin.top])
        .nice()
    )

    return svg
