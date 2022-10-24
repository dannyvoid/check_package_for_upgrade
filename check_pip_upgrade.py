import os, sys, shutil, pip
import luddite
from pkg_resources import parse_version, get_distribution, DistributionNotFound

auto_upgrade = []


def package_installed(package):
    try:
        get_distribution(package)
        return True
    except DistributionNotFound:
        return False


def install_package(package):
    if input(f"Do you want to install {package}? (y/n): ") == "y":
        pip.main(["install", package])
        print(f"{package} installed")
    else:
        print(f"{package} not installed")


def upgrade_package(package):
    local_version = get_distribution(package).version
    remote_version = luddite.get_version_pypi(package)

    if local_version == remote_version:
        print(f"{package} is up to date (local: {local_version})")
    else:
        if parse_version(local_version) < parse_version(remote_version):
            print(
                f"{package} is out of date (local: {local_version} < remote: {remote_version})"
            )

        if parse_version(local_version) > parse_version(remote_version):
            print(
                f"{package} is newer than remote (local: {local_version} > remote: {remote_version})"
            )

        print(f"local: {local_version}")
        print(f"remote: {remote_version}")

        if package in auto_upgrade:
            print(f"Auto upgrading {package}")
            pip.main(["install", "--upgrade", package])
            print(f"{package} upgraded")
        else:
            if input("Do you want to upgrade? (y/n): ") == "y":
                pip.main(["install", "--upgrade", package])
                print(f"{package} upgraded")
            else:
                print(f"{package} not upgraded")


def fix_corrupted_package():
    site_packages = os.path.join(os.path.dirname(os.__file__), "site-packages")
    site_packages = os.path.normpath(site_packages)

    if os.path.exists(site_packages):
        for package in os.listdir(site_packages):
            if package.startswith("~"):
                shutil.rmtree(os.path.join(site_packages, package))


def main():
    if len(sys.argv) > 1:
        package_list = sys.argv[1:]
    else:
        package_list = input(
            "Enter a package name (seperate multiple package names by space): "
        )

    if isinstance(package_list, str):
        package_list = package_list.split()

    for package in package_list:
        if package_installed(package):
            upgrade_package(package)
        else:
            print(f"{package} is not installed")
            fix_corrupted_package()
            install_package(package)


if __name__ == "__main__":
    main()
