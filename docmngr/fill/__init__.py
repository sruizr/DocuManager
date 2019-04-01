import uuid
import fs.copy
import fs.path
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

        with self.fs.open(template_path, 'r') as f:
            source = f.read()

        return source, template_path, lambda: True


class Filler:
    """Filler helper to inherits depending of text outut
    """
    def __init__(self, docu_service, template_dir='/templates', env_config=None):
        template_fs = docu_service.fs.opendir(template_dir)
        env_config = env_config if env_config else {}
        self.engine = Environment(loader=FSLoader(template_fs),
                                  **env_config)

        self.fs = docu_service.fs
        docu_service.temp_fs.makedirs('/filled_files', recreate=True)
        self._temp_fs = docu_service.temp_fs.opendir('/filled_files')

    def fill(self, data, template_path, destination_path):
        """Fill data on template and return a temporary file path
        """
        template = self.engine.get_template(template_path)
        text_content = template.render(**data)

        template_ext = fs.path.basename(template_path).split('.')[-1]
        filled_fn = '{}.{}'.format(str(uuid.uuid4()), template_ext)

        with self._temp_fs.open(filled_fn, 'w') as f:
            f.write(text_content)

        self.convert(filled_fn, destination_path)

    def convert(self, filled_fn, destination_path):
        fs.copy.copy_file(self._temp_fs, filled_fn, self.fs, destination_path)
