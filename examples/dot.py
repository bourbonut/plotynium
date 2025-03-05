from sklearn.datasets import load_iris
import polars as pl

import plotynium as ply

iris = load_iris()
df = pl.DataFrame(iris.data, schema=iris.feature_names)
df = df.insert_column(df.width, pl.Series("species", iris.target))
# ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']

plot = ply.plot(
    marks=[
        ply.dot(
            df.to_dicts(),
            x="sepal length (cm)",
            y="sepal width (cm)",
            stroke="species",
        )
    ],
    color={"scheme": ply.Scheme.CATEGORY_10}
)

with open("dot.svg", "w") as file:
    file.write(str(plot))
