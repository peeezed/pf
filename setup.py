from setuptools import setup,find_packages


def get_requirements():
    with open("requirements.txt") as reqs:
        content = reqs.read()
        requirements = content.split("\n")
    return requirements


setup(
    name = "builder",
    version = "0.1",
    packages = find_packages(),
    include_package_data = True,
    install_requires = get_requirements(),
    entry_points = """
        [console_scripts]
        builder=builder.cli:cli
    """
)