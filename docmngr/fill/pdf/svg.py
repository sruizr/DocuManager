from .. import BaseFiller
import subprocess


class SvgFiller(BaseFiller):
    def convert(self, origin_path, destination_path):
        temp_path = origin_path.replace('.svg', '.pdf')

        self.temp_fs(or)
        base = ['inkscape']
        svg_input = ['-f', svg_path_file]
        pdf_output = ['-A', pdf_path_file]

        command = base + svg_input + pdf_output
        subprocess.check_call(command)

        self.destination_fs.copy()

        return destination_path
