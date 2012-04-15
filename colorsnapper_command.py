import sublime
import sublime_plugin
import subprocess
from os import path

class PickWithColorSnapperCommand(sublime_plugin.TextCommand):
    """
    Runs ColorSnapper externall application and replaces
    selected text with a picked color code.
    Attpemts to automatically recognize CSS format from selection.
    """

    def run(self, edit):
        format = False
        view = self.view
        self.settings = sublime.load_settings('ColorSnapper.sublime-settings')

        # Determine in which format to pick
        if self.settings.get('autoFormat'):
            sel = view.sel()
            if len(sel) > 0:
                selected = view.substr(view.word(sel[0])).strip()
                if (selected.startswith('#')):
                    format = 'cssHEXUpper'

        # Pick a color
        color = self.run_color_picker(format)

        # If got a string with color
        if color:
            # For each selected region
            for region in view.sel():
                # get a word from region
                word = view.word(region)
                # see if it's a color in HEX format and if it starts with #
                if self.is_valid_hex_color(view.substr(word)) and view.substr(word.a - 1) == '#':
                    # increase selection to include '#'
                    word = sublime.Region(word.a - 1, word.b)
                    # and replace it with picked color
                    view.replace(edit, word, str(color))
                else:
                    # otherwise just replace selection
                    view.replace(edit, region, str(color))

    def run_color_picker(self, format):
        args = str(self.settings.get("path"))
        if not format:
            if self.settings.has("format"):
                args += ' --format ' + str(self.settings.get("format"))
        else:
            args += ' --format ' + str(format)

        if self.settings.has("magnification"):
            args += ' -m ' + str(self.settings.get("magnification"))

        try:
            process = subprocess.Popen( args,
                                        shell   = True,
                                        stdout  = subprocess.PIPE,
                                        stderr  = subprocess.PIPE
                                      )
            result, error = process.communicate()
            if error != '':
                sublime.error_message(error.decode('utf-8'))
            else:
                return result.decode('utf-8')

        except OSError, error:
            sublime.error_message(error.decode('utf-8'))

    def is_valid_hex_color(self, s):
      if len(s) not in (3, 6):
        return False
      try:
        return 0 <= int(s, 16) <= 0xffffff
      except ValueError:
        return False
