"""
Internal utilities to replace external dependencies.
"""
import inspect
import os
import platform
import sys
import ctypes
import types
if platform.system() == "Windows":
    try:
        import win32com.client
    except ImportError:
        win32com = None
else:
    win32com = None

def is_frozen():
    """
    Returns True if the application is running as a frozen executable 
    (py2exe, pyinstaller, cx_freeze, etc.)
    """
    # imp was removed in Python 3.12, but _imp still contains is_frozen.
    # This is what cffi uses.
    try:
        import _imp
        return hasattr(sys, "frozen") or '__compiled__' in globals() or _imp.is_frozen("__main__")
    except ImportError:
        return hasattr(sys, "frozen") or '__compiled__' in globals()

def get_executable():
    """Returns the full executable path/name if frozen, or the full path/name of the main module if not."""
    if is_frozen():
        if platform.system() != "Darwin":
            return sys.executable
        # On Mac, sys.executable points to python. We want the full path to the exe we ran.
        exedir = os.path.abspath(os.path.dirname(sys.executable))
        items = os.listdir(exedir)
        if "python" in items:
            items.remove("python")
        return os.path.join(exedir, items[0])
    # Not frozen
    try:
        import __main__
        return os.path.abspath(__main__.__file__)
    except AttributeError:
        return sys.argv[0]

def executable_directory():
    """Always determine the directory of the executable, even when run with py2exe or otherwise frozen"""
    # Check for PyInstaller
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    executable = get_executable()
    path = os.path.abspath(os.path.dirname(executable))
    return path

def embedded_data_path():
    """Get the path where embedded data files are stored"""
    if platform.system() == "Darwin" and is_frozen():
        return os.path.join(os.path.abspath(get_executable()), 'Contents', 'MacOS')
    return executable_directory()

def get_module(level=2):
    """Hacky method for deriving the caller of this function's module."""
    return inspect.getmodule(inspect.stack()[level][0]).__file__

def module_path(level=2):
    """Get the path of the calling module"""
    return os.path.abspath(os.path.dirname(get_module(level)))

def load_library(libname, cdll=False):
    """
    Load a DLL library with ctypes.
    
    Args:
        libname: Name of the library file
        cdll: If True, use cdll (for __cdecl), otherwise use windll (for __stdcall)
    
    Returns:
        ctypes library object
    """
    if is_frozen():
        libfile = os.path.join(
            embedded_data_path(), "accessible_output3", "lib", libname
        )
    else:
        libfile = os.path.join(module_path(), "lib", libname)
    
    if not os.path.exists(libfile):
        _cxfreeze_libfile = os.path.join(
            embedded_data_path(), "lib", "accessible_output3", "lib", libname
        )
        if os.path.exists(_cxfreeze_libfile):
            libfile = _cxfreeze_libfile
    
    if cdll:
        return ctypes.cdll[libfile]
    return ctypes.windll[libfile]

def load_com(*names):
    """
    Load a COM object using win32com.client.
    
    Args:
        *names: One or more names to try for the COM object
    
    Returns:
        COM object instance
    
    Raises:
        ImportError: If win32com is not available
        TypeError: If COM object cannot be created
    """
    if not hasattr(win32com, 'client'):
        raise ImportError("pywin32 is required for COM functionality")
    
    for name in names:
        try:
            return win32com.client.Dispatch(name)
        except:
            continue
    
    # If we get here, none of the names worked
    raise TypeError(f"Could not create COM object with any of the provided names: {names}")

# Compatibility classes for libloader.com module access
class ComModule:
    """Compatibility class to provide the same interface as libloader.com"""
    def load_com(self, *names):
        return load_com(*names)

# Create a module-like object for backward compatibility
com = types.ModuleType('com')
com.load_com = load_com
