import os

def read_file(file_path):
    """Read the contents of a file and return as a string."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_path} not found."
    except IOError:
        return f"Error: Unable to read {file_path}."

def write_file(file_path, content):
    """Write content to a file, overwriting existing content."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Content successfully written to {file_path}"
    except IOError:
        return f"Error: Unable to write to {file_path}."

def append_to_file(file_path, content):
    """Append content to an existing file."""
    try:
        with open(file_path, 'a') as file:
            file.write(content)
        return f"Content successfully appended to {file_path}"
    except IOError:
        return f"Error: Unable to append to {file_path}."

def file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path)

def delete_file(file_path):
    """Delete a file."""
    try:
        os.remove(file_path)
        return f"{file_path} has been deleted."
    except FileNotFoundError:
        return f"Error: {file_path} not found."
    except IOError:
        return f"Error: Unable to delete {file_path}."

def get_file_size(file_path):
    """Get the size of a file in bytes."""
    try:
        return os.path.getsize(file_path)
    except FileNotFoundError:
        return f"Error: {file_path} not found."
    except IOError:
        return f"Error: Unable to retrieve size for {file_path}."
