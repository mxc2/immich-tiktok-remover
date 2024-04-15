import subprocess
import re

def get_package_sizes():
    # Get a list of all installed packages
    installed_packages = subprocess.check_output(['pip', 'freeze']).decode().split('\n')

    # Iterate over each installed package
    for package in installed_packages:
        # Extract package name
        package_name = package.split('==')[0]
        
        # Get package information
        output = subprocess.check_output(['pip', 'show', '--files', package_name]).decode()
        
        # Extract file paths and sizes
        file_info = re.findall(r'^\s*([^:]+):\s*([\d,]+)\s+bytes', output, re.MULTILINE)
        
        # Calculate total size
        total_size = sum(int(size.replace(',', '')) for _, size in file_info)
        
        # Print package name and total size
        print(f"{package_name}: {total_size} bytes")

if __name__ == "__main__":
    get_package_sizes()
