import polars as pl
from sklearn import datasets, manifold
import plotynium as plot

nsamples = 1500
spoints, scolors = datasets.make_s_curve(nsamples, random_state=0)

params = {
    "n_neighbors": 12,
    "n_components": 2,
    "eigen_solver": "auto",
    "random_state": 0,
}
lle_methods = [
    ("Standard locally linear embedding", "standard"),
    ("Local tangent space alignment", "ltsa"),
    ("Hessian eigenmap", "hessian"),
    ("Modified locally linear embedding", "modified"),
]

plots = {}
for title, method in lle_methods:
    lle = manifold.LocallyLinearEmbedding(method=method, **params)
    points = lle.fit_transform(spoints)
    df = pl.from_numpy(points, schema=["colx", "coly"]).insert_column(
        2, pl.Series("color", scolors)
    )
    data = df.to_dicts()
    plots[title] = plot.plot(marks=[plot.dot(data, x="colx", y="coly", stroke="color")])

for i, (_, plot) in enumerate(plots.items()):
    with open(f"{lle_methods[i][1]}.svg", "w") as file:
        file.write(str(plot))
