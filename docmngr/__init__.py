from dependency_injection import DynamicContainer
from fs.temporary import TemporaryFS


class DocuManager:
    def __init__(self, **config):
        "docstring"
        self.fs = file_system
        self.temp_fs = TemporaryFS()

    def _load_fillers(self, fillers):
        pass

    def _load_file_systems(self, file_systems):
        pass

    def fill(self, data, template, docu_path):
        pass

    def print_doc(self, printer_name, fs, path):
        pass

    def export(self, source_path, destination_path=None, fs_name=None):
        pass
