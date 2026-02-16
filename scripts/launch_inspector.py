#!/usr/bin/env python3
"""
Quick launcher script for Appium Inspector.
Can be run directly or imported as a module.
"""

from src.main.utils.appium_inspector_launcher import AppiumInspectorLauncher


def launch_inspector(verbose=False):
    """
    Launch Appium Inspector with optional verbose output.

    Example usage in test files:
        from scripts.launch_inspector import launch_inspector
        launch_inspector(verbose=True)
    """
    launcher = AppiumInspectorLauncher(verbose=verbose)
    return launcher.launch()


if __name__ == "__main__":
    import sys
    success = launch_inspector(verbose=True)
    sys.exit(0 if success else 1)
