import fs.copy
import subprocess
from .. import BaseFiller


class SvgFiller(BaseFiller):
    def convert(self, origin_path, destination_path):
        svg_sys_path = self.temp_fs.getsyspath(origin_path)
        pdf_sys_path = svg_sys_path.replace('.svg', '.pdf')

        base = ['inkscape']
        svg_input = ['-f', svg_path_file]
        pdf_output = ['-A', pdf_path_file]
        command = base + svg_input + pdf_output
        subprocess.check_call(command)

        pdf_path = origin_path.replace('.svg', '.pdf')

        fs.copy.copy_file(
            self.temp_fs, pdf_path,
            self.out_fs, destination_path
        )
