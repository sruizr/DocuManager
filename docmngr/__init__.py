import subprocess
from fs.temporary import TemporaryFS
from fs.copy import copy_file

_CLASS_NAMES ={
    'tex2pdf': 'docmngr.fillers.pdf.tex.Filler',
    'svg2pdf': 'docmngr.fillers.pdf.svg.Filler'
}


class DocuManager:
    def __init__(self, file_system, **config):
        "docstring"
        self.fs = file_system

        self.temp_fs = TemporaryFS()
        self._temp_paths = {}
        self._fillers = {}

    def _load_filler(self, fillers):
        pass
from fs.tempfs import TempFS
import fs.copy
import fs.path
import time
import logging


logger = logging.getLogger(__name__)

_FILLERS = {
    'tex2pdf': 'docmngr.fillers.pdf.tex.Filler',
    'svg2pdf': 'docmngr.fillers.pdf.svg.Filler'
}


class DocuService:
    def __init__(self, file_system, root_path):
        "docstring"
        self.fs = file_system.opendir(root_path)
        self.temp_fs = TempFS()
        self.fillers = {}
        self._temp_files = {}

    def _load_filler(self, key):
        Filler = __import__(_FILLERS[key])
        self.filler[key] = Filler(self)

    def fill(self, data, template_name, docu_path):
        logger.info('filled document {}'.format(docu_path))
        # template_type = template_name.split('.')[-1]
        # doc_type = docu_path.split('.')[-1]

        # filler_key = '{}2{}'.format(template_type, doc_type)
        # if filler_key not in self.fillers:  # Lazzy loading
        #     self._load_filler(filler_key)

        # filler = self.fillers[filler_key]
        # filler.fill(data, template_name, docu_path)

    def getsyspath(self, path):
        if path in self._temp_files:
            return self._temp_files[path]

        if self.fs.hassyspath(path):
            return self.fs.getsyspath(path)
        else:
            dirname = fs.path.dirname(path)
            if not self.temp_fs.isdir(dirname):
                self.temp_fs.makedirs(dirname, recreate=True)

            fs.copy.copy_file(self.fs, path,
                              self.temp_fs, path)
            logger.info('Copied {} file to temporary fs'.format(path))

            self._temp_files[path] = self.temp_fs.getsyspath(path)
            return self._temp_files[path]

    def print_to_cups_printer(self, printer_name, file_path):
        """Print to cups printer using command line
        """
        path = self.getsyspath(file_path)
        command = 'lp -d {} "{}"'.format(printer_name, path)
        subprocess.check_call(command, shell=True)

    def export(self, source_path, fs, destination_path=None):
        destination_path = destination_path if destination_path else source_path
        fs.copy.copy_file(self.fs, source_path, fs, destination_path)

    def __del__(self):
        self.temp_fs.close()
        self.fs.close()
