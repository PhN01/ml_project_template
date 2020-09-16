import yaml


class Config(object):
    def __init__(self) -> None:

        self.data_dir = ""

    def load(self, file_path: str) -> None:
        with open(file_path, "r") as f:
            c = yaml.load(f, Loader=yaml.FullLoader)
        for name, value in c.items():
            self.__setattr__(name, value)
        self.update_dynamic_attributes()

    def save(self, file_path: str) -> None:
        with open(file_path, "w") as f:
            yaml.dump(self.__dict__, f, indent=4)

    def update_dynamic_attributes(self) -> None:
        pass
