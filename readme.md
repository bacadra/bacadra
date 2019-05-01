# bacadra

## Main goal

FEM package for civil engineering task's with extensive resources helpful during calculation like report generators, small calculation sheets etc.

The project is developing very dynamically and a lot of information may be out of date.

## How to install

The long-term update channel is provide by PyPi index. To install last relase just type below command. At the moment this source is not maintained.

~~~shell
pip install bacadra
~~~

To install latest version, includng hotfixes etc. just type below command (you must have already installed git software).

~~~shell
pip install git+https://github.com/bacadra/bacadra
~~~

## How to start

If you have already install package then type simple import statment in your favourite python editor.

~~~python
import bacadra as bcdr
~~~

bacadra software provide also customable units package, which object set is already defined in depend package. To use SI system type get object from si file.

~~~python
from bacadara.unise.si import *
~~~

## `core` package

Most functions can be found in the `core` package.

~~~python
b0 = bcdr.core   # provide interface to manage new one project
b1 = bcdr.core() # create project
~~~

The structure of the core package:

* `unise` - units for structural engineering,
* `dbase` - database menagment,
* `tools` - system and project tools,
    * `verrs` - variable errors; manage bacadra errors, warnings and infos,
    * `erwin` - errors, warnings, infos; call new one,
    * `fpack` - full pack of tools which are project independt,
    * `clang` - choose language for project purpose,
* `pinky` - report makers,
    * `docme` - ms word document generator,
    * `texme` - latex document generator,
    * `fstme` - fast report document generator,
* `sofix` - cross of bacadra and SOFiSTiK,
    * `sbase` - SOFiSTiK database connection,
    * `wgraf` - WiNGRAF connection; autopic generator,
    * `trade` - trade variables between SOFiSTiK and bacadra kernels,
* `bapps` - bacadra application.


