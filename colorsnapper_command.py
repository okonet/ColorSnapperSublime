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

        # Pick a color
        color = self.run_color_picker()

        # For each selected region
        for region in view.sel():
            # get a word from region
            word = view.word(region)
            # see if it's a color in HEX format
            if self.is_valid_hex_color(view.substr(word)):
                # and if it starts with #
                if view.substr(word.a - 1) == '#':
                    # increase selection to include '#'
                    word = sublime.Region(word.a - 1, word.b)
                    # and replace it with picked color
                    view.replace(edit, word, str(color))
            else:
                # otherwise just replace selection
                view.replace(edit, region, str(color))

    def run_color_picker(self):
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
                return result.decode('utf-8')

        except OSError, error:
            sublime.errorMessage(error.decode('utf-8'))

    def is_valid_hex_color(self, s):
      if len(s) not in (3, 6):
        return False
      try:
        return 0 <= int(s, 16) <= 0xffffff
      except ValueError:
        return False
