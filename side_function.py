import os
import re
import pandas as pd

def search_files(directory, file_type, sub_name=None, title=None):
    """
    Search for files in a directory that match a list of subjects (sub_name) and report missing subjects.

    Args:
        directory (str): Path to the directory to search.
        file_type (str): File type to search for (e.g., ".tsv", ".csv").
        sub_name (list or None): List of subjects to search for (default is None, meaning no filtering).
        title (str or None): Title for logging, default is None.

    Returns:
        tuple: (List of matching files, List of missing subjects, Updated list of subjects after excluding missing ones).
    """
    print("_______________________________________________________")
    print(f"\n{title}")
    if sub_name:
        print(f"\nNumber of input subjects: {len(sub_name)} subjects")

    matched_files = []  # List to store paths of matching files
    missing_subs = set(sub_name) if sub_name else set()  # Set of subjects not yet found

    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has the specified type
            if file.endswith(file_type):
                file_path = os.path.join(root, file)

                # If sub_name is provided, check if the file matches any subject in sub_name
                if sub_name:
                    for sub in sub_name:
                        if sub in file:  # Match subject name in file
                            matched_files.append(file_path)  # Add matching file to the list
                            missing_subs.discard(sub)  # Remove found subject from missing_subs

    # Report results
    print(f"\nMatched subjects: {len(matched_files)} subjects")

    if sub_name and missing_subs:
        print(f"\nMissing subjects: {len(missing_subs)} subjects")
        for sub in missing_subs:
            print(sub)
    else:
        missing_subs = set()  # Ensure missing_subs is an empty set if sub_name is None

    # Update sub_name by excluding missing subjects
    updated_subs = [sub for sub in sub_name if sub not in missing_subs] if sub_name else None
    print(f"\nUpdated subject: {len(updated_subs) if updated_subs else 0} subjects")

    print("______________________________")

    return matched_files, updated_subs


def search_subnums(directory, prefix="sub", separator="-", id_length=8):
    """
    Extract subject codes from all filenames in the directory.

    Args:
        directory (str): Path to the directory containing the files.
        prefix (str): The prefix of the subject code (default is 'sub').
        separator (str): The character between the prefix and ID (e.g., '-' or '_').
        id_length (int): The length of the ID following the prefix (default is 8).

    Returns:
        list: A list of found subject codes.
    """
    # Regular expression pattern to find the subject code
    pattern = rf"{prefix}{separator}\w{{{id_length}}}"
    subnums = []

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        match = re.search(pattern, filename)
        if match:
            subnums.append(match.group())

    print(f"\nNumber of subject codes found: {len(subnums)}\n")
    return subnums


def get_subject_list(file_path, data_type=1):
    """
    Get a list of participant IDs based on the value(s) of the data_collection column.

    Args:
        file_path (str): Path to the input data file.
        data_type (int or list): Value(s) of the data_collection column to filter by. 
                                 Can be a single integer or a list of integers.

    Returns:
        list: List of participant IDs matching the condition.
    """
    # Read data from the TSV file
    data = pd.read_csv(file_path, sep="\t")

    # Filter participant IDs based on the data_collection value(s)
    if isinstance(data_type, list):
        selected_subjects = data[data['data_collection'].isin(data_type)]['participant_id'].tolist()
    else:
        selected_subjects = data[data['data_collection'] == data_type]['participant_id'].tolist()

    print(f"\nNumber of subjects found: {len(selected_subjects)}\n")
    return selected_subjects


def search_files_v2(directory, file_type, sub_name=None, title=None):
    """
    Search for files in a directory that match a list of subjects (sub_name) and report missing subjects.
    If sub_name is None, search for all files with the specified file_type.

    Args:
        directory (str): Path to the directory to search.
        file_type (str): File type to search for (e.g., ".tsv", ".csv").
        sub_name (list or None): List of subjects to search for (default is None, meaning no filtering).
        title (str or None): Title for logging, default is None.

    Returns:
        tuple: (List of matching files, List of missing subjects, Updated list of subjects after excluding missing ones).
    """
    print("_______________________________________________________")
    print(f"\n{title}")
    if sub_name:
        print(f"\nNumber of input subjects: {len(sub_name)} subjects")
    else:
        print("\nDo not have input sub_name list")

    exist_files = []
    matched_files = []  # List to store paths of matching files
    missing_subs = set(sub_name) if sub_name else set()  # Set of subjects not yet found

    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has the specified type
            if file.endswith(file_type):
                file_path = os.path.join(root, file)
                exist_files.append(file_path)   

                if sub_name:
                    # Check if the file matches any subject in sub_name
                    for sub in sub_name:
                        if sub in file:  # Match subject name in file
                            matched_files.append(file_path)  # Add matching file to the list
                            missing_subs.discard(sub)  # Remove found subject from missing_subs
                    
                else:
                    # If no sub_name is provided, add all files of the specified type
                    matched_files.append(file_path)

    print(f"\nExist subjects in folder ({file_type}): {len(exist_files)} subjects")
    # Report results
    print(f"\nMatched subjects ({file_type}): {len(matched_files)} subjects")

    if sub_name and missing_subs:
        print(f"\nMissing subjects ({file_type}): {len(missing_subs)} subjects")
        for sub in missing_subs:
            print(sub)
    else:
        missing_subs = set()  # Ensure missing_subs is an empty set if sub_name is None

    # Update sub_name by excluding missing subjects
    updated_subs = [sub for sub in sub_name if sub not in missing_subs] if sub_name else None
    print(f"Updated subject ({file_type}): {len(updated_subs) if updated_subs else 0} subjects")

    print("______________________________")

    return matched_files, updated_subs

def search_files_v3(directory, file_type, sub_name=None, title=None):
    """
    Search for files in a directory that match a list of subjects (sub_name) 
    and report missing and extra subjects.

    Args:
        directory (str): Path to the directory to search.
        file_type (str): File type to search for (e.g., ".tsv", ".csv").
        sub_name (list or None): List of subjects to search for (default is None, meaning no filtering).
        title (str or None): Title for logging, default is None.

    Returns:
        tuple: (List of matching files, List of missing subjects, Updated list of subjects, List of extra subjects).
    """
    print("_______________________________________________________")
    print(f"\n{title}")
    if sub_name:
        print(f"\nNumber of input subjects: {len(sub_name)} subjects")
    else:
        print("\nDo not have input sub_name list")

    exist_files = []
    matched_files = []  # List to store paths of matching files
    missing_subs = set(sub_name) if sub_name else set()  # Set of subjects not yet found
    extra_subs = set()  # Set to store extra subjects in directory

    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has the specified type
            if file.endswith(file_type):
                file_path = os.path.join(root, file)
                exist_files.append(file_path)
                file_name = os.path.basename(file)
                
                if sub_name:
                    # Check if the file matches any subject in sub_name
                    matched = False
                    for sub in sub_name:
                        if sub in file_name:  # Match subject name in file
                            matched_files.append(file_path)  # Add matching file to the list
                            missing_subs.discard(sub)  # Remove found subject from missing_subs
                            matched = True
                            break
                    
                    # If the file does not match any input subject, add it to extra_subs
                    if not matched:
                        extra_subs.add(file_name.split('.')[0])  # Add subject ID (without extension)

                else:
                    # If no sub_name is provided, add all files of the specified type
                    matched_files.append(file_path)

    # Report existing files
    print(f"\nExist subjects in folder ({file_type}): {len(exist_files)} files")
    # Report matched files
    print(f"\nMatched subjects ({file_type}): {len(matched_files)} files")

    # Report missing subjects
    if sub_name and missing_subs:
        print(f"\nMissing subjects ({file_type}): {len(missing_subs)} subjects")
        for sub in sorted(missing_subs):
            print(sub)
    else:
        missing_subs = set()

    # Report extra subjects
    if extra_subs:
        print(f"\nExtra subjects in directory ({file_type}): {len(extra_subs)} subjects")
        for sub in sorted(extra_subs):
            print(sub)

    # Update sub_name by excluding missing subjects
    updated_subs = [sub for sub in sub_name if sub not in missing_subs] if sub_name else None
    print(f"\nUpdated subjects ({file_type}): {len(updated_subs) if updated_subs else 0} subjects")

    print("______________________________")

    return matched_files, updated_subs