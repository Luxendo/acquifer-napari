# acquifer-napari

[![License](https://img.shields.io/pypi/l/acquifer-viewer.svg?color=green)](https://github.com/LauLauThom/acquifer-viewer/raw/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/acquifer-viewer.svg?color=green)](https://pypi.org/project/acquifer-viewer)
[![Python Version](https://img.shields.io/pypi/pyversions/acquifer-viewer.svg?color=green)](https://python.org)
[![tests](https://github.com/LauLauThom/acquifer-viewer/workflows/tests/badge.svg)](https://github.com/LauLauThom/acquifer-viewer/actions)
[![codecov](https://codecov.io/gh/LauLauThom/acquifer-viewer/branch/master/graph/badge.svg)](https://codecov.io/gh/LauLauThom/acquifer-viewer)

Visualize IM datasets as a multi-dimensional image, using lazy data-loading thanks to Dask. 

This [napari] plugin was generated with [Cookiecutter] using with [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started
-->

## Configurations
The file `napari.yaml` in `acquifer_napari_plugin` defines what functions of the python package are visible to napari.  
The top level `name` field must be the same than the python package name defined in `setup.cfg`.
It first define a set of commands, which have a custom `id`, and a `python_name`, which is the actual location of the function in the python package (or module).  
Then the napari.yaml has optional subsections `readers`, `writers`, `widget`, to reference some of the commands previously defined, to notify napari that they implemente those standard functions.  
For instance I first define a command myReader pointing to myPackage.myReader, and I reference that command using the id it in the section readers  
See https://napari.org/stable/plugins/first_plugin.html#add-a-napari-yaml-manifest  

## Installation
The plugin can be installed from source by downloading this repo, opening a conda prompt in the repo directory and calling:  
`pip install .` or `pip install --user .` if user permission is an issue.  

Use `pip install -e .` to install in developement mode, so any change in the source code is directly reflected.  
Use `npe2 list` to check that the plugin is correctly installed and visible by napari.  
For instance here, the package defines 1 command, which is a reader.  
One could have more commands, which would be implement other types.   
This should output something like following 
┌──────────────────────────────┬─────────┬──────┬───────────────────────────────────────────────────────────┐
│ Name                         │ Version │ Npe2 │ Contributions                                             │
├──────────────────────────────┼─────────┼──────┼───────────────────────────────────────────────────────────┤
│ acquifer-napari              │ 0.0.1   │ ✅   │ commands (1), readers (1)

The plugin should be installed in an environment with napari installed.  
Napari can be started with the `napari`command in a command prompt with a system wide python installation.  
Once installed, napari can be opened in a IPython interactive session with

```python
>> import napari
>> napari.Viewer()
```
The acquifer-napari plugin loads IM04 datasets, and display each channel as a separate "layer" in napari.  
Sliders for well, channel, time and Z are automatically rendered when there are more than 1 coordinates along the dimension.  


## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin
[file an issue]: https://github.com/LauLauThom/acquifer-viewer/issues
[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
