from libs.libraries import libraries
from libs.libraryInstaller import libsCheck

# Check for requiements libraries and install if not installed
for libs in libraries:
    libsCheck(libs)
