import subprocess
import sys


def check_local_pip(package):
    import re
    pip_show = f"python -m pip show {package}"
    version = subprocess.check_output(pip_show, shell=True)
    version = version.decode('utf-8')
    version = re.findall(r'\d+\.\d+\.\d+', version)
    version = version[0]
    return version


def check_remote_pip(package):
    import luddite
    version = luddite.get_version_pypi(package)
    return version


def main(package):
    local_version = check_local_pip(package)
    remote_version = check_remote_pip(package)
    if local_version == remote_version:
        print(f"{package} is up to date (local: {local_version})")
    else:
        print(f"{package} is out of date (local: {local_version} < remote: {remote_version})")
        print(f"local: {local_version}")
        print(f"remote: {remote_version}")

        if input("Do you want to upgrade? (y/n): ") == 'y':
            subprocess.call(f"python -m pip install --upgrade {package}", shell=True)
            print(f"{package} upgraded")
        else:
            print(f"{package} not upgraded")


if __name__ == "__main__":
    package = sys.argv[1]
    main(package)