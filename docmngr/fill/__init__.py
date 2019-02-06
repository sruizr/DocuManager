import fs.copy
from fs.tempfs import TempFS
from jinja2.loaders import BaseLoader, TemplateNotFound
from jinja2 import Environment


class FSLoader(BaseLoader):
    """Loader for FileSystem object (PyFileSystem interface)
    """
    def __init__(self, fs):
        "docstring"
        self.fs = fs

    def get_source(self, environment, template_path):
        if not self.fs.exists(template_path):
            raise TemplateNotFound(template_path)

        source = self.fs.readtext(template_path)

        return source, template_path, lambda: True


class BaseFiller:
    """Filler helper to inherits depending of text outut
    """
    def __init__(self, template_fs, out_fs):
        self.temp_fs = TempFS()
        self.engine = Environment(loader=FSLoader(template_fs))
        self.out_fs = out_fs

    def fill(self, data, template_path, destination_path):
        """Fill data on template and return a temporary file path
        """
        template = self.engine.get_template(template_path)
        text_content = template.render(**data)

        with self._temp_fs.open(destination_path, 'w') as f:
            f.write(text_content)

        return self._temp_fs.getsyspath(destination_path)

    def convert(self, source_path, destination_path):
        """Command to convert from templated format to final format
        """
        fs.copy.copy_file(self.tempfs, source_path,
                          self.out_fs, destination_path)
