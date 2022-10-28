import os, sys, shutil, subprocess
import luddite
from pkg_resources import parse_version, get_distribution, DistributionNotFound


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
    version = get_version(package, "remote")
    name_version = f'"{package}" ({version})'

    if auto_install:
        print(f"Auto installing {name_version}")
        subprocess.run(["pip", "install", package])
        print(f"{name_version} installed")
    else:
        if input(f"Do you want to install {name_version}? (y/n): ") == "y":
            subprocess.run(["pip", "install", package])
            print(f"{name_version} installed")
        else:
            print(f"{name_version} not installed")


def get_version(package, type):
    types = ["local", "remote"]
    if type not in types:
        raise ValueError(f"type must be one of: {types}")
    elif type == "local":
        return get_distribution(package).version
    elif type == "remote":
        return luddite.get_version_pypi(package)


def upgrade_package(package):
    local_version = get_version(package, "local")
    remote_version = get_version(package, "remote")

    if compare_versions(local_version, remote_version, package) != 0:
        print(f"local: {local_version}")
        print(f"remote: {remote_version}")

        if package in []:
            install_package(package, auto_install=True)
        else:
            install_package(package)


def fix_corrupted_package():
    dirs = subprocess.check_output(["python", "-m", "site", "--user-site"])
    dirs = dirs.decode("utf-8").split(os.linesep)
    dirs = [os.path.normpath(dir) for dir in dirs if os.path.exists(dir)]

    for directory in dirs:
        for package in os.listdir(directory):
            if package.startswith("~"):
                if input(f"Do you want to delete {package}? (y/n): ") == "y":
                    shutil.rmtree(os.path.join(directory, package))
                    print(f"{package} deleted")
                else:
                    print(f"{package} not deleted")


def main():
    if len(sys.argv) > 1:
        package_list = sys.argv[1:]
    else:
        package_list = input("Enter packages (seperate multiple names by space): ")

    if isinstance(package_list, str):
        package_list = package_list.split()

    fix_corrupted_package()

    for package in package_list:
        if package_installed(package):
            upgrade_package(package)
        else:
            print(f"{package} is not installed")
            install_package(package)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
