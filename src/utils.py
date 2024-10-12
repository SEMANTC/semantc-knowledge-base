import os
import yaml
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("yaml_loader.log"),
        logging.StreamHandler()
    ]
)

def iterate_yaml_files(directory, reformat=True):
    """
    Generator function to iterate through all YAML files in a directory.
    
    Args:
        directory (str): Path to the knowledge base directory.
        reformat (bool): Whether to reformat YAML content - defaults to True.
    
    Yields:
        str or dict: YAML content as a string if reformat is True, else as a dictionary.
    """
    if not os.path.isdir(directory):
        logging.error(f"The directory {directory} does not exist or is not a directory.")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.yml', '.yaml')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        yaml_content = yaml.safe_load(f)
                    
                    if yaml_content is None:
                        logging.warning(f"YAML file {file_path} is empty.")
                        continue

                    if reformat:
                        # Convert the YAML content back to a standardized string format
                        standardized_yaml = yaml.dump(yaml_content, default_flow_style=False, sort_keys=False)
                        logging.info(f"Processed and standardized YAML file: {file_path}")
                        yield standardized_yaml
                    else:
                        # Yield the parsed YAML content as a dictionary
                        logging.info(f"Loaded YAML file as dictionary: {file_path}")
                        yield yaml_content
                except yaml.YAMLError as e:
                    logging.error(f"YAML parsing error in file {file_path}: {e}")
                except Exception as e:
                    logging.error(f"Error reading file {file_path}: {e}")