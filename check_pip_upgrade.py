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
        for package in os.listdir(site_packages):
            if package.startswith("~"):
                shutil.rmtree(os.path.join(site_packages, package))


def package_installed(package):
    try:
        pkg_resources.get_distribution(package)
        return True
    except pkg_resources.DistributionNotFound:
        return False


def install_package(package):
    if input(f"Do you want to install {package}? (y/n): ") == "y":
        subprocess.call(f"python -m pip install {package}", shell=True)
        print(f"{package} installed")
    else:
        print(f"{package} not installed")


def get_local_package_version(package):
    version = subprocess.check_output(f"python -m pip show {package}", shell=True)
    version = version.decode("utf-8")
    version = re.findall(r"Version: (.*)", version)[0]
    version = re.sub(r"[^\d.]", "", version)
    return version


def get_remote_package_version(package):
    version = luddite.get_version_pypi(package)
    version = re.sub(r"[^\d.]", "", version)
    return version


def upgrade_package(package):
    local_version = get_local_package_version(package)
    remote_version = get_remote_package_version(package)

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
        package_list = sys.argv[1:]
    else:
        package_list = input(
            "Enter a package name (seperate multiple package names by space): "
        )

    if isinstance(package_list, str):
        package_list = package_list.split()

    if "pip" not in package_list:
        package_list.insert(0, "pip")

    for package in package_list:
        package = re.sub(r"[^\w.-]", "", package)

        if package_installed(package):
            upgrade_package(package)
        else:
            print(f"{package} is not installed")
            fix_corrupted_package()
            install_package(package)


if __name__ == "__main__":
    main()
