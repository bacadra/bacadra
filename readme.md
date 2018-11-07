# bacadra

## Main goal

FEM package for civil engineering task's.


## How to install

The long-term update channel is provide by PyPi index. To install last relase just type below command.
~~~
pip install bacadra
~~~

On the otherhand, to install latest version, includng hotfixes etc. just type below command (you must have already installed git software).
~~~
pip install git+https://github.com/bacadra/bacadra
~~~


## How to start

If you have already install package then type simple import statment in your favourite python editor.
~~~
import bacadra as bcdr
~~~

bacadra software provide also customable units package, which object set is already defined in depend package. To use SI system type get object from si file.

~~~
from bacadara.cunit.si import *
~~~

or to use CE (Civil Engineering) system type get object from si file.

~~~
from bacadara.cunit.ce import *
~~~

Additional import math function which was customize to full compability with cunit.

~~~
from bacadara.cunit.cmath import *
~~~


# Report maker

The main part of report maker zone is package `pinky`. It depend on LaTeX language or MS Word language (in process...).


# FEM project

## `project` class
To initialize FEM project type project class. It join all FEM-root packages, provide link to central database (SQLite technology).

~~~
p = bcdr.project()
~~~

## `dbase` class

The main goal of `dbase` class is provide interface to work with SQLite relational database. We can create local database (extension `.bcdr` recommended) or create it in memory (`.path = :memory:`).

~~~
p.dbase.path = 'main.bcdr'
p.dbase.connect()
...
p.dbase.close()
~~~

While database is creating, the full table relative ssodb is creating.
