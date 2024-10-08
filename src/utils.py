import os
import yaml

def iterate_yaml_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yml') or file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    yaml_content = yaml.safe_load(f)
                    # convert the YAML content to a string
                    yield yaml.dump(yaml_content, default_flow_style=False)