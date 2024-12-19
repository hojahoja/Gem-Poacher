from utilities.config_manager import ConfigManager


def generate_config():
    config_manager = ConfigManager()
    config_manager.create_config(force=True)


if __name__ == "__main__":
    generate_config()
