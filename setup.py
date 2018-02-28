from setuptools import setup

VERSION = "0.0.2"
DEPS = [
         "boto3",
         "boutiques"
       ]

setup(name="clowdr",
      version=VERSION,
      description="Tool for launching pipelines locally and remotely",
      url="http://github.com/clowdr/clowdr",
      author="Gregory Kiar",
      author_email="gkiar07@gmail.com",
      classifiers=[
                "Programming Language :: Python",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.5",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: Implementation :: PyPy",
                "License :: OSI Approved :: MIT License",
                "Topic :: Software Development :: Libraries :: Python Modules",
                "Operating System :: OS Independent",
                "Natural Language :: English"
                  ],
      license="MIT",
      packages=["clowdr"],
      include_package_data=True,
      test_suite="pytest",
      tests_require=["pytest"],
      setup_requires=DEPS,
      install_requires=DEPS,
      entry_points = {
        "console_scripts": [
            "clowdr=clowdr.driver:main",
        ]
      },
      zip_safe=False)