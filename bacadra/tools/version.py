'''
------------------------------------------------------------------------------
BCDR += ***** (version)ing pattern *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


import re
def is_canonical(version):
    return re.match(r'^v([1-9]\d*!)?(0|[1-9]\d*)(\.(0|[1-9]\d*))*((a|b|rc)(0|[1-9]\d*))?(\.post(0|[1-9]\d*))?(\.dev(0|[1-9]\d*))?$', version) is not None

is_canonical('v0.1')
is_canonical('v0.2.dev1')
is_canonical('v0.2a1')
