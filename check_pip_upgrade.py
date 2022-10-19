import subprocess
import sys
import os
import shutil
import pkg_resources
import luddite
import re

auto_upgrade = ["pip"]


def fix_corrupted_package():
    site_packages = os.path.join(os.path.dirname(os.__file__), "site-packages")
    site_packages = os.path.normpath(site_packages)

    if os.path.exists(site_packages):
        packages = os.listdir(site_packages)
        packages = [package for package in packages if package.startswith("~")]

    if packages:
        for package in packages:
            package = os.path.join(site_packages, package)
            package = os.path.normpath(package)
            shutil.rmtree(package)
        return

    else:
        return


def check_if_package_installed(package):
    try:
        pkg_resources.get_distribution(package)
        return True
    except pkg_resources.DistributionNotFound:
        return False


def install_package(package):
    subprocess.call(f"python -m pip install {package}", shell=True)


def check_local_package(package):
    version = subprocess.check_output(f"python -m pip show {package}", shell=True)
    version = version.decode("utf-8")
    version = re.findall(r"Version: (.*)", version)[0]
    return version


def check_remote_package(package):
    version = luddite.get_version_pypi(package)
    return version


def upgrade_package(package):
    local_version = re.sub(r"[^\d.]", "", check_local_package(package))
    remote_version = re.sub(r"[^\d.]", "", check_remote_package(package))

    if local_version == remote_version:
        print(f"{package} is up to date (local: {local_version})")
    else:
        print(
            f"{package} is out of date (local: {local_version} < remote: {remote_version})"
        )
        print(f"local: {local_version}")
        print(f"remote: {remote_version}")

        if package in auto_upgrade:
            print(f"Auto upgrading {package}")
            subprocess.call(f"python -m pip install --upgrade {package}", shell=True)
            print(f"{package} upgraded")

        else:
            if input("Do you want to upgrade? (y/n): ") == "y":
                subprocess.call(
                    f"python -m pip install --upgrade {package}", shell=True
                )
                print(f"{package} upgraded")
            else:
                print(f"{package} not upgraded")


def main():
    if len(sys.argv) > 1:
        package = sys.argv[1]
    else:
        package = input("Enter a package name: ")

    package = package.split()[0]

    if package != "pip":
        upgrade_package("pip")

    if not check_if_package_installed(package):
        fix_corrupted_package()
        install_package(package)

    upgrade_package(package)


if __name__ == "__main__":
    main()
