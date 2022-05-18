import sys

from cx_Freeze import Executable, setup

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("core/app.py", base=base)]
includefiles = ['./materials']

setup(
    name="simple_Tkinter",
    version="0.1",
    description="Sample cx_Freeze Tkinter script",
    options={'build_exe': {'include_files': includefiles}},
    executables=executables,
)
