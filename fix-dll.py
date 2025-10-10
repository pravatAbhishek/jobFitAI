import os
import subprocess
import sys

def fix_numpy_dll():
    print("Upgrading pip, setuptools, wheel...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    print("Uninstalling potentially broken packages...")
    for pkg in ["numpy", "scipy", "scikit-learn"]:
        subprocess.call([sys.executable, "-m", "pip", "uninstall", "-y", pkg])

    print("Reinstalling clean versions...")
    for pkg in ["numpy", "scipy", "scikit-learn"]:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", pkg])

    print("All done! Try running your code again.")

if __name__ == "__main__":
    fix_numpy_dll()
