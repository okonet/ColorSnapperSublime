import sublime
import sublime_plugin
import subprocess

class PickWithColorSnapperCommand(sublime_plugin.TextCommand):
    """
    Runs ColorSnapper externall application and replaces
    selected text with a picked color code.
    Attpemts to automatically recognize CSS format from selection.
    """

    def run(self, edit):
        view = self.view
        args = "~/Downloads/ColorSnapper.app/Contents/MacOS/ColorSnapper cli --format cssHEXUpper -m 2"
        try:
            process = subprocess.Popen( args,
                                        shell   = True,
                                        stdout  = subprocess.PIPE,
                                        stderr  = subprocess.PIPE
                                      )
            result, error = process.communicate()
            if error != '':
                sublime.errorMessage(error.decode('utf-8'))
            else:
                for region in view.sel():
                    view.replace(edit, region, str(result.decode('utf-8')))

        except OSError, error:
            sublime.errorMessage(error.decode('utf-8'))

        edit.end_edit()
