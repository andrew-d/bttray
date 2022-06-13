import os
import setuptools


requires = [
    'pulsectl',
    'PyGObject',
]

_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_ROOT, 'README.md')) as f:
    long_description = f.read()


setuptools.setup(
    name="bttray",
    version="0.0.1",
    description="Simple tray icon to swap Bluetooth headset modes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Andrew Dunham",
    author_email="andrew@du.nham.ca",
    url="https://github.com/andrew-d/bttray",
    download_url="https://github.com/andrew-d/bttray/archive/v0.0.1.tar.gz",
    packages=setuptools.find_packages(),
    install_requires=requires,
    entry_points={'console_scripts': ['bttray = bttray.__main__:main']},
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities"
    ] + [('Programming Language :: Python :: %s' % x) for x in '3 3.5 3.6 3.7 3.8 3.9'.split()]
)
