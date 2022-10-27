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


def compare_versions(local, remote, package):
    if parse_version(local) == parse_version(remote):
        print(f"{package} is up to date.", end=" ")
        print(f"(local: {local})")
        return 0

    if parse_version(local) < parse_version(remote):
        print(f"{package} is out of date.", end=" ")
        print(f"(local: {local} < remote: {remote})")
        return 1

    if parse_version(local) > parse_version(remote):
        print(f"{package} is newer than remote.", end=" ")
        print(f"(local: {local} > remote: {remote})")
        return -1


def install_package(package, auto_install=False):
    if auto_install:
        print(f"Auto installing {package}")
        pip.main(["install", package])
        print(f"{package} installed")
    else:
        if input(f"Do you want to install {package}? (y/n): ") == "y":
            pip.main(["install", package])
            print(f"{package} installed")
        else:
            print(f"{package} not installed")


def upgrade_package(package):
    local_version = get_distribution(package).version
    remote_version = luddite.get_version_pypi(package)

    if compare_versions(local_version, remote_version, package) != 0:
        print(f"local: {local_version}")
        print(f"remote: {remote_version}")

        if package in auto_upgrade:
            install_package(package, auto_install=True)
        else:
            install_package(package)


def fix_corrupted_package(directory):
    directory = os.path.normpath(directory)

    if os.path.exists(directory):
        for package in os.listdir(directory):
            if package.startswith("~"):
                if input(f"Do you want to delete {package}? (y/n): ") == "y":
                    shutil.rmtree(os.path.join(directory, package))
                    print(f"{package} deleted")
                else:
                    print(f"{package} not deleted")
    else:
        print(f"{directory} does not exist")


def main():
    if len(sys.argv) > 1:
        package_list = sys.argv[1:]
    else:
        package_list = input("Enter packages (seperate multiple names by space): ")

    if isinstance(package_list, str):
        package_list = package_list.split()

    fix_corrupted_package(
        os.path.normpath(os.path.join(os.path.dirname(os.__file__), "site-packages"))
    )

    for package in package_list:
        if package_installed(package):
            upgrade_package(package)
        else:
            print(f"{package} is not installed")
            install_package(package)


if __name__ == "__main__":
    main()
