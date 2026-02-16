import os
import sys
import platform
import subprocess
import json
from pathlib import Path


class AppiumInspectorLauncher:
    """
    Launches Appium Inspector on the local machine.
    Supports macOS, Linux, and Windows.
    Auto-installs appium-inspector via npm if not present.
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.system = platform.system()
        self.inspector_name = "appium-inspector"

    def log(self, message):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[AppiumInspector] {message}")

    def _npm_available(self) -> bool:
        """Check if npm is available on the system."""
        try:
            subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                check=True,
                timeout=5
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _inspector_installed(self) -> bool:
        """Check if appium-inspector is installed globally."""
        try:
            subprocess.run(
                ["npm", "list", "-g", self.inspector_name],
                capture_output=True,
                check=True,
                timeout=10
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _install_inspector(self) -> bool:
        """Install appium-inspector globally via npm."""
        if not self._npm_available():
            print("Error: npm is not installed or not in PATH")
            print("Please install Node.js from https://nodejs.org/")
            return False

        print(f"Installing {self.inspector_name} globally...")
        try:
            subprocess.run(
                ["npm", "install", "-g", self.inspector_name],
                check=True,
                timeout=300  # 5 minute timeout
            )
            self.log(f"{self.inspector_name} installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to install {self.inspector_name}")
            print(f"Command failed with exit code {e.returncode}")
            return False
        except subprocess.TimeoutExpired:
            print(f"Error: Installation timed out")
            return False

    def _get_inspector_path(self) -> str:
        """Get the full path to appium-inspector executable."""
        try:
            result = subprocess.run(
                ["npm", "list", "-g", "--depth=0", "--parseable", self.inspector_name],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            base_path = result.stdout.strip()
            if not base_path:
                return None

            # Construct path based on OS
            if self.system == "Windows":
                return os.path.join(base_path, "bin", "appium-inspector.cmd")
            else:
                return os.path.join(base_path, "bin", "appium-inspector")
        except Exception as e:
            self.log(f"Error getting inspector path: {e}")
            return None

    def _launch_macos(self, inspector_path) -> bool:
        """Launch Appium Inspector on macOS using 'open' command."""
        try:
            subprocess.Popen(["open", "-a", "Appium Inspector"])
            return True
        except FileNotFoundError:
            self.log("'open' command not found on macOS")
            return False

    def _launch_linux(self, inspector_path) -> bool:
        """Launch Appium Inspector on Linux."""
        try:
            subprocess.Popen([inspector_path])
            return True
        except FileNotFoundError:
            self.log(f"Executable not found at {inspector_path}")
            return False

    def _launch_windows(self, inspector_path) -> bool:
        """Launch Appium Inspector on Windows."""
        try:
            subprocess.Popen(inspector_path, shell=True)
            return True
        except FileNotFoundError:
            self.log(f"Executable not found at {inspector_path}")
            return False

    def launch(self) -> bool:
        """
        Launch Appium Inspector. Auto-installs if not present.
        Returns True if successful, False otherwise.
        """
        self.log(f"System: {self.system}")

        # Check and install if needed
        if not self._inspector_installed():
            print(f"{self.inspector_name} not found. Installing...")
            if not self._install_inspector():
                return False

        self.log(f"{self.inspector_name} is installed")

        # Get path to executable
        inspector_path = self._get_inspector_path()
        if not inspector_path:
            print(f"Error: Could not determine path to {self.inspector_name}")
            return False

        self.log(f"Inspector path: {inspector_path}")

        # Launch based on OS
        print(f"Launching Appium Inspector...")
        try:
            if self.system == "Darwin":  # macOS
                success = self._launch_macos(inspector_path)
            elif self.system == "Linux":
                success = self._launch_linux(inspector_path)
            elif self.system == "Windows":
                success = self._launch_windows(inspector_path)
            else:
                print(f"Error: Unsupported operating system: {self.system}")
                return False

            if success:
                print("✓ Appium Inspector launched successfully")
                return True
            else:
                print("✗ Failed to launch Appium Inspector")
                return False

        except Exception as e:
            print(f"Error: Failed to launch inspector: {e}")
            return False


def main():
    """CLI entry point for launching Appium Inspector."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Launch Appium Inspector on your machine. "
                    "Auto-installs via npm if not present."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    launcher = AppiumInspectorLauncher(verbose=args.verbose)
    success = launcher.launch()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
