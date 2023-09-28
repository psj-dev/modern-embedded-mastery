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

    # Get a list of topic directories at the root of the project (excluding dotfiles)
    topics = [dir for dir in next(os.walk(root_path))[1] if not dir.startswith('.')]

    # Print the list of topics with numbers
    print('Topics:')
    for i, topic_name in enumerate(topics, start=1):
        print(f'{i}. {topic_name}')

    # Initialize an empty dictionary to hold the table of contents for each directory
    tables_of_contents = {}

    for topic_name in topics:
        # Get a list of subtopic directories in the current topic directory
        subtopics = [dir for dir in next(os.walk(os.path.join(root_path, topic_name)))[1] if not dir.startswith('.')]

        # Print the list of subtopics with numbers
        print(f'\nSubtopics for {topic_name}:')
        for i, subtopic_name in enumerate(subtopics, start=1):
            print(f'{i}. {subtopic_name}')

        for subtopic_name in subtopics:
            # Use a glob pattern to find 'table of contents.md' files in the current content directory
            toc_path = glob.glob(os.path.join(root_path, topic_name, subtopic_name, 'table of contents.md'))
            if toc_path:
                # Read the contents of the 'table of contents.md' file
                with open(toc_path[0], 'r') as f:
                    toc_contents = f.read()
                # Store the contents in the dictionary, using the subtopic directory name as the key
                if subtopic_name in tables_of_contents:
                    tables_of_contents[subtopic_name] += '\n' + toc_contents
                else:
                    tables_of_contents[subtopic_name] = toc_contents

    # Replace each tag in the stub contents with the corresponding table of contents
    for subtopic_name, toc_contents in tables_of_contents.items():
        tag = '{' + subtopic_name + '}'
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
