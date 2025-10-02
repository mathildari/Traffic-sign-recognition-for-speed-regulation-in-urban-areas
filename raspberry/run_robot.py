#!/usr/bin/env python3
"""
Entry point to run the Raspberry Pi robot from detected traffic signs.
"""
import sys
from raspberry.robot_run import main

if __name__ == "__main__":
    sys.exit(main())