from .. import Filler as BaseFiller
import fs.copy
import subprocess


class Filler(BaseFiller):
    def __init__(self , docu_service, template_dir='/templates'):
        "docstring"
        env_config = {
            'block_start_string': '\BLOCK{',
            'block_end_string': '}',
            'variable_start_string': '\VAR{',
            'variable_end_string': '}',
            'comment_start_string': '\#{',
            'comment_end_string': '}',
            'line_statement_prefix': '%%',
            'line_comment_prefix': '%#',
            'trim_blocks': True,
            'autoescape': False
        }

        super().__init__(docu_service, template_dir, env_config)

    def convert(self, filled_fn, destination_path, run_many=2):
        """Converts filled file to pdf file
        """
        filled_syspath = self._temp_fs.getsyspath(filled_fn)

        output_directory = self._temp_fs.getsyspath('/')
        for _ in range(run_many):
            command = "pdflatex -output-directory {} {}".format(output_directory,
                                                         filled_syspath)
            subprocess.check_call(command, shell=True)

        pdf_fn = filled_fn.replace('.tex', '.pdf')

        fs.copy.copy_file(self._temp_fs, pdf_fn, self.fs, destination_path)
