import platform
platform.mac_ver = lambda: ('14.0', ('', '', ''), 'arm64')

import sys
from pip._internal.cli.main import main

if __name__ == '__main__':
    sys.exit(main())
