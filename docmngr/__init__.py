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

    def _load_file_systems(self, file_systems):
        pass

    def fill_to_pdf(self, data, template, docu_path):
        template_type = template.split('.')[-1]
        filler_key = '{}2pdf'.format(template_type)
        if filler_key not in self._fillers:
            Filler = __import__(_CLASS_NAMES[filler_key])
            template_fs
            self._fillers[filler_key] = Filler()



    def print_to_cups_printer(self, printer_name, file_path):
        """Print file from
        """
        full_filename = self.get_sys_path(file_path)
        command = 'lp -D {} {}'.format(printer_name, full_filename)
        subprocess.check_output(command)

    def getsyspath(self, path):
        if self.fs.hassyspath(path):
            return self.fs.get_sys_path(path)
        else:
            if path not in self._temp_paths:
                copy_file(self.fs, path, self.temp_fs, path)
                self._temp_paths[path] = self.temp_fs.getsyspath(path)

            return self._temp_paths[path]

    def export_file(self, file_path, fs_name, destination_path=None):
        """Export file to named filsystem
        """
        destination_path = destination_path if destination_path else file_path

        to_fs = self.file_systems[fs_name]
        copy_file(self.fs, file_path, to_fs, destination_path)
