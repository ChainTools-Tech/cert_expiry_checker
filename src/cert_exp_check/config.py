import yaml


def load_config(config_path):
    """Simplified function to load YAML configuration file"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)