import os


def find_file(searched, path='.'):
    """
    Find a file at a given path

    args :
        - searched : str, searched file
        - path : str, base path, by default : '.'
    returns :
        - str, path to the searched file


    >>> find_file('diagnosis_covid19')
    '.\\Data\\diagnosis_covid19'
    """

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.startswith(searched):
                return os.path.join(root, file)

            