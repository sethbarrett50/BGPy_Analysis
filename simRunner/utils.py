import os
import re
import time

from functools import wraps

# RegEx pattern for directory naming
pattern = re.compile(r"\.([^.>]*)(?='>|$)")


def __nameMaker(s): return pattern.search(s).group(1)  # Lamda for getting names for dir creation


def timing_decorator(func):
    '''
    Decorator to calc & print time to run a func
    '''
    @wraps(func)
    def __wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.4f} seconds to complete")
        return result
    return __wrapper


def dirMaker(configDict: dict) -> str:
    '''
    Creates a directory path based on the given configuration dictionary.

    Constructs a directory path using the 'policy', 'scenario', and 'asType' values from the provided configuration dictionary. If the directory already exists, raises a FileExistsError. Otherwise, creates the directory and returns its path.

    Args:
        configDict (dict): Dictionary containing user-selected configurations for 'policy', 'scenario', and 'asType'.

    Returns:
        str: The path to the created directory.

    Raises:
        FileExistsError: If the directory already exists.
    '''
    simOutputDir = f'./simOutput/'
    if configDict["policy"] == "AS-Cones":
        simOutputDir += f'{configDict["policy"]}'
    else:
        simOutputDir += {__nameMaker(str(configDict["policy"]))}

    if configDict["scenario"] == 'ForgedOriginSubPrefix':
        simOutputDir += f'{configDict["scenario"]}'
    else:
        simOutputDir += f'{__nameMaker(str(configDict["scenario"]))}'

    if configDict["asType"] == 'NoDeploymentType':
        simOutputDir += f'{configDict["asType"]}'
    else:
        simOutputDir += f'{__nameMaker(str(configDict["asType"]))}'

    if os.path.exists(simOutputDir):
        raise FileExistsError(
            f"The directory '{simOutputDir}' already exists.")
    os.makedirs(simOutputDir)

    return simOutputDir


def main():
    print("File should not be run this way")


if __name__ == '__main__':
    main()
