# acquifer-viewer

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

and review the napari docs for plugin developers:
https://napari.org/docs/plugins/index.html
-->

## Installation
The plugin can be installed from source by downloading this repo, opening a conda prompt in the repo directory and calling:  
`pip install .` or `pip install --user .` if user permission is an issue.  

Obviously the plugin should be installed in an environment with napari already.  
Once installed, napari can be opened in a IPython interactive session with

```python
>> import napari
>> napari.Viewer()
```
Then one can activate the acquifer-viewer plugin via the menu `Plugins > Install/Uninstall packages`.  
Also clicking the *Show Sorter* button will display the list of hooks available.  
Selecting `get_reader`in the list of hooks should list the acquifer-viewer hook (preferentially in 1st position).  
From there on, anytime `File > Open Folder` is used in napari, it will use the acquifer-viewer to load it.  

The acquifer-viewr loads IM04 datasets, and display each channel as a separate "layer" in napari.  
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
