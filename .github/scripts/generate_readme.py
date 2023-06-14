import os
import glob
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate README.md from table of contents.md files')
parser.add_argument('root_path', type=str, help='Root path of the project')
args = parser.parse_args()

try:
    # Path to the __README.stub file and root path
    stub_path = os.path.join(args.root_path, '.github/__README.stub')
    root_path = args.root_path

    # Read the contents of the stub file
    with open(stub_path, 'r') as f:
        stub_contents = f.read()

    # Get a list of directories at the root of the project (excluding dotfiles)
    dirs = [dir for dir in next(os.walk(root_path))[1] if not dir.startswith('.')]

    # Initialize an empty dictionary to hold the table of contents for each directory
    tables_of_contents = {}

    for dir_name in dirs:
        # Get a list of content directories in the current topic directory
        content_dirs = [dir for dir in next(os.walk(os.path.join(root_path, dir_name)))[1] if not dir.startswith('.')]
        for content_dir in content_dirs:
            # Use a glob pattern to find 'table of contents.md' files in the current content directory
            toc_path = glob.glob(os.path.join(root_path, dir_name, content_dir, 'table of contents.md'))
            if toc_path:
                # Read the contents of the 'table of contents.md' file
                with open(toc_path[0], 'r') as f:
                    toc_contents = f.read()
                # Store the contents in the dictionary, using the content directory name as the key
                if content_dir in tables_of_contents:
                    tables_of_contents[content_dir] += '\n' + toc_contents
                else:
                    tables_of_contents[content_dir] = toc_contents

    # Replace each tag in the stub contents with the corresponding table of contents
    for content_dir, toc_contents in tables_of_contents.items():
        tag = '{' + content_dir + '}'
        stub_contents = stub_contents.replace(tag, toc_contents)

    # Write the final contents to the 'README.md' file
    with open(os.path.join(root_path, 'README.md'), 'w') as f:
        f.write(stub_contents)
        
except FileNotFoundError as e:
    print(f"File not found: {e}")
except IOError as e:
    print(f"IO error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
