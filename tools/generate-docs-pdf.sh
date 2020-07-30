#!/bin/bash
pdoc3 --pdf gezeiten > docs/gezeiten.md

# Remove first 2 lines (random pygame output)
sed -i -e 1,2d docs/gezeiten.md

pandoc --metadata=title:"Gezeitenreibung - Computational Physics - Documentation" --metadata=author:"Bennet Weiss, Nico Alt" --toc --toc-depth=4 --from=markdown+abbreviations --pdf-engine=xelatex --variable=mainfont:"DejaVu Sans" --output=docs/gezeiten.pdf docs/gezeiten.md
