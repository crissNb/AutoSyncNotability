import configparser
from pathlib import Path

class ConfigReader:
    def load_config(self) -> configparser.ConfigParser:
        parser = configparser.ConfigParser()

        # check if config file exists and then load
        if not Path("~/.config/AutoSyncNotability/config.ini").expanduser().is_file():
            print("Config file not found. Creating one...")
            # create config file
            parser['DEFAULT'] = {
                'regex_match': '',
                'reference_path': '',
            }

            # create new folder for config file
            Path("~/.config/AutoSyncNotability").expanduser().mkdir(parents=True, exist_ok=True)

            with open(Path("~/.config/AutoSyncNotability/config.ini").expanduser(), 'w') as configfile:
                parser.write(configfile)

        parser.read(Path("~/.config/AutoSyncNotability/config.ini").expanduser())
        return parser
