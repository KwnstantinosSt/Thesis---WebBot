import subprocess
import sys
import pkg_resources

# Install packages


def installPackage(package):
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package])
        print(
            f"The {package} installed succefully or already installed and up to date..")
    except Exception as ex:
        print(f"Error {ex}")
    finally:
        print("Closing library installer...")

# Check Libraries


def libsCheck(name):
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s" % (i.key)
                                      for i in installed_packages])
    if name in installed_packages_list:
        return True
    else:
        installPackage(name)
        return
