import subprocess
import sys


def check_local_package(package):
    import re
    version = subprocess.check_output(f"python -m pip show {package}", shell=True)
    version = version.decode('utf-8')
    version = re.findall(r'\d+\.\d+\.\d+', version)
    version = version[0]
    return version


def check_remote_package(package):
    import luddite
    version = luddite.get_version_pypi(package)
    return version


def upgrade_package(package):
    local_version = check_local_package(package)
    remote_version = check_remote_package(package)
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


def main():
    if len(sys.argv) > 1:
        package = sys.argv[1]
        upgrade_package(package)
    else:
        package = input("Enter a package name: ")
        upgrade_package(package)
        input("Press enter to exit")


if __name__ == "__main__":
    main()
