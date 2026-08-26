"""install_kernel.py -- registers JEWEL as a real Jupyter kernelspec.

Run with the jupyter venv's own python: /home/fatbaby/.venvs/jupyter/bin/python install_kernel.py
"""

import json
import os
import sys

from jupyter_client.kernelspec import KernelSpecManager

HERE = os.path.dirname(os.path.abspath(__file__))

KERNEL_JSON = {
    "argv": [sys.executable, os.path.join(HERE, "jewel_kernel.py"), "-f", "{connection_file}"],
    "display_name": "PARENA (JEWEL)",
    "language": "parena",
}


def main():
    spec_dir = os.path.join(HERE, "_kernelspec_build", "jewel")
    os.makedirs(spec_dir, exist_ok=True)
    with open(os.path.join(spec_dir, "kernel.json"), "w") as f:
        json.dump(KERNEL_JSON, f, indent=2)

    ksm = KernelSpecManager()
    dest = ksm.install_kernel_spec(spec_dir, kernel_name="jewel", user=True, replace=True)
    print(f"Installed JEWEL kernelspec at: {dest}")


if __name__ == "__main__":
    main()
