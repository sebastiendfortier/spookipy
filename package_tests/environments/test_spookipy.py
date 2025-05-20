#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for spookipy package in different Python environments.
"""

import sys


def run_test():
    """Run tests for spookipy functionality."""
    try:
        import spookipy
        import spookipy.filterdigital

        print(f"\nPython version: {sys.version}")
        print(f"Testing spookipy version: {spookipy.__version__}")
        return spookipy.__version__ == "2025.03.00"
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False


if __name__ == "__main__":
    success = run_test()
    print("✅ Great Success!" if success else "❌ Deported!")
    sys.exit(0 if success else 1)
