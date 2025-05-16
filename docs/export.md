1. Convert the `figure.svg` to `figure.pdf_tex

```bash
inkscape -D figure.svg -o figure.pdf --export-latex
```

2. Change the font size with the following command:

```bash
sed -i 's/\\\f@size/ 7.5/g' figure.pdf_tex"
```

3. Create a file `file.tex` and add the following content:

```latex
\documentclass{article}
\usepackage{color}
\usepackage{graphicx}

\begin{document}

\begin{figure}[!ht]
  \centering
  \def\svgwidth{\columnwidth}
  \scalebox{0.8}{\input{figure.pdf_tex}}
  \caption{Cool figure}
\end{figure}

\end{document}
```

4. Compile the LaTeX file:

```bash
pdflatex file.tex
```
