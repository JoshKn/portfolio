# Experimental script using Python's filecmp.dircmp to compare the Casting DB media and convertedmedia directories.
# Prints files only present in one of the directories (left_only / right_only) and files differing in content.

# phind dircmp program
import filecmp
import os

def test(dir1, dir2):
    comparision = filecmp.dircmp(dir1, dir2)

    print(type(comparision))

def compare_directories(dir1, dir2):
    # Create a Dircmp object to compare the two directories
    comparison_converted = filecmp.dircmp(dir1, dir2)
    comparison_backup = filecmp.dircmp(dir1, dir3)
    
    # Print files unique to dir1
    if comparison.left_only:
        print(f"Files in '{dir1}' but not in '{dir2}':")
        for file in comparison.left_only:
            print(file)
    
    # Print files unique to dir2
    if comparison_converted.right_only:
        print(f"\nFiles in '{dir2}' but not in '{dir1}':")
        for file in comparison.right_only:
            print(file)
    
    # Print files differing in content
    if comparison.diff_files:
        print("\nFiles differing in content:")
        for file in comparison.diff_files:
            print(file)
    
    # Recursively compare subdirectories
    for subdir in comparison.common_dirs:
        compare_directories(os.path.join(dir1, subdir), os.path.join(dir2, subdir))

# Example usage
dir1 = "path\\to\\media\\"
dir2 = "path\\to\\convertedmedia\\"
dir3 = "\\\\nas-server\\backup\\"

#compare_directories(dir1, dir2)
test(dir1, dir2)