from setuptools import setup


def get_requirements_from_file():
    with open("./requirements.txt") as f_in:
        requirements = f_in.read().splitlines()
    return requirements


setup(
    name="mylib",
    version="0.0.2",
    author="khides",
    author_email="taikoud29study@gmail.com",
    description="only calculation",
    # package_dir={"": ""},
    install_requires=get_requirements_from_file()
)
