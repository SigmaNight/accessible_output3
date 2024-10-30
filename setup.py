from setuptools import setup, find_packages
import io

__doc__ = (
    """Library to provide speech and braille output to a variety of different screen readers and other accessibility solutions."""
)

with io.open("readme.rst", encoding="UTF8") as readme:
    long_description = readme.read()

setup(
    name="accessible_output3",
    author="Luna R",
    author_email="pypi@lvna.me",
    version="0.1.2",
    description=__doc__,
    long_description=long_description,
    package_dir={"accessible_output3": "accessible_output3"},
    packages=find_packages(),
    package_data={"accessible_output3": ["lib/*"]},
    zip_safe=False,
    install_requires=[
        "libloader",
        "platform_utils @ git+https://github.com/accessibleapps/platform_utils.git@e0d79f7b399c4ea677a633d2dde9202350d62c38",
        "winpaths @ git+https://github.com/Accessiware/winpaths.git@57eb1f0fb45e150391463263598b0ac18eb171eb"
    ],
    extras_require={
        ':sys_platform == "win32"': ["pywin32", "libloader"],
        ':sys_platform == "darwin"': ["appscript"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Adaptive Technologies",
        "Topic :: Software Development :: Libraries",
    ],
)
