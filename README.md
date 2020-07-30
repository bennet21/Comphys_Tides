# Comphys Project 2020 - Bennet and Nico

This is Bennet Weiss' and Nico Alt's project for Computational Physics created in 2020.
More information can be found in
[Nico's blog post](https://nico.dorfbrunnen.eu/posts/2020/physics/)
and in [the report](report.pdf).

## Running

Development happens with Pycharm, so it's best to just clone the repository and import it there.

To run this program without 3D animations, you need to install the Python dependencies:
```bash
pip3 install -r requirements.txt
```

On Debian/elementary/Ubuntu/etc. you can use _apt_ instead of _pip_:
```bash
sudo apt install python3-numpy python3-matplotlib python3-scipy
```

You can then start the program by calling `./gezeiten.py`.

### 3D animations

To render the 3D animation of the earth-moon system, you need to install two more dependencies:

```bash
# With pip
pip3 install -r requirements-animations.txt

# On Debian/elementary/Ubuntu/etc.
sudo apt install python3-opengl python3-pygame
```

You can then start the animations by calling `./gezeiten-animations.py`. You can navigate in space
using your keyboard.

The source code of the animations is based on the project
[SolarSystem](https://github.com/elbanic/SolarSystem) by elbanic. Kudos to them!

#### Keyboard navigation

You can always go back to the default view by pressing `space`. Other navigation options include:

* arrow keys to turn left, right, up, down
* `a` and `s` to zoom in and out
* `e` and `r` to rotate into positive and negative direction of _x_
* `q` and `w` to rotate into positive and negative direction of _y_

## Documentation

The documentation of the project's code can be found in the _docs_ directory.
To update it, call `tools/generate-docs-html.sh`. To generate a PDF of the docs, call
`tools/generate-docs-pdf.sh`. Note that you need the Python package `pdoc3` and the system packages
`pandoc` and `texlive-xetex` to make the updates work.

## License

Everything is licensed under AGPL-3.0. See [LICENSE.md](LICENSE.md) for more information.
