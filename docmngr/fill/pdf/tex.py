from .. import Filler as BaseFiller
import fs.copy
import subprocess


class Filler(BaseFiller):
    def __init__(self , docu_service, template_dir='/templates'):
        "docstring"
        env_config = {
            block_start_string: '\BLOCK{',
	    block_end_string: '}',
	    variable_start_string: '\VAR{',
	    variable_end_string: '}',
	    comment_start_string: '\#{',
	    comment_end_string: '}',
	    line_statement_prefix: '%%',
	    line_comment_prefix: '%#',
	    trim_blocks: True,
	    autoescape: False
        }

        super().__init__(docu_service, template_dir, env_config)

    def convert(self, filled_fn, destination_path):
        filled_path = self._temp_fs.getsyspath(filled_fn)
        command = ["pdflatex"]
        subprocess.check_call(com, shell=True)


        pdf_fn = '{}.pdf'.format(filled_fn.split())
