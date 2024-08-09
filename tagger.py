import os
import re
from mutagen.flac import FLAC

def set_event_and_date_tags(directory):
    # Compile the regex patterns
    date_pattern = re.compile(r'^(?P<date>\d{4}\.\d{2}\.\d{2})')
    tag_pattern = re.compile(r'\[([^\[\]]+)\]$')
    
    file_count = 0  # Initialize the counter

    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            date_match = date_pattern.match(dir_name)
            tag_match = tag_pattern.search(dir_name)
            
            if date_match and tag_match:
                date_value = date_match.group('date')
                tag_value = tag_match.group(1)
                dir_path = os.path.join(root, dir_name)

                # Recursively scan for FLAC files in the matched directory
                for sub_root, _, sub_files in os.walk(dir_path):
                    for file_name in sub_files:
                        if file_name.lower().endswith('.flac'):
                            file_path = os.path.join(sub_root, file_name)
                            flac_file = FLAC(file_path)
                            modified = False

                            # Check if the 'EVENT' tag exists
                            if 'EVENT' not in flac_file:
                                flac_file['EVENT'] = tag_value
                                print(f"Added 'EVENT' tag with value '{tag_value}' to: {file_path}")
                                modified = True

                            # Check if the 'DATE' tag exists
                            if 'DATE' not in flac_file:
                                flac_file['DATE'] = date_value
                                print(f"Added 'DATE' tag with value '{date_value}' to: {file_path}")
                                modified = True
                            
                            if modified:
                                flac_file.save()

                            # Increment the file counter
                            file_count += 1
                            if file_count % 250 == 0:
                                print(f"Scanned {file_count} files so far")

    print(f"Total files scanned: {file_count}")

if __name__ == "__main__":
    base_directory = './'
    set_event_and_date_tags(base_directory)
