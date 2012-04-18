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
        word = False
        view = self.view
        original_sel = view.sel()
        self.settings = sublime.load_settings('ColorSnapper.sublime-settings')

        # Determine in which format to pick
        if self.settings.get('autoFormat'):
            # Get selections
            sel = view.sel()
            if len(sel) > 0:
                if len(sel[0]) > 0: # If selection contains more than 1 symbol we will not modify it
                    format = self.recognize_format(view.substr(sel[0]).strip())
                else: # otherwise
                    # let's try HEX firstly
                    word = view.word(sel[0]) # select a word
                    if self.is_valid_hex_color(view.substr(word).strip()) and view.substr(word.a - 1) == '#':
                        if self.settings.has("upperCaseHEX") and self.settings.get("upperCaseHEX"):
                            format = 'cssHEXUpper'
                        else:
                            format = 'cssHEX'
                        word = sublime.Region(word.a - 1, word.b)
                    else:
                        # Expand selection to brackets if any
                        view.run_command('expand_selection', {'to': 'brackets', 'brackets': '[,('})
                        # and when expand selection to include brackets
                        view.run_command('expand_selection', {'to': 'brackets', 'brackets': '[,('})
                        brackets_sel = view.sel()[0]
                        brackets_str = view.substr(brackets_sel).strip()
                        if len(brackets_str) > 0: # if there selected text in it it probably one of a complex formats. Let's check for it
                            format = self.recognize_format(brackets_str)
                            if not format: # it's not NSColor or UIColor
                                brackets_reg = sublime.Region(brackets_sel.a - 3, brackets_sel.b)
                                format = self.recognize_from_region(brackets_reg)
                                if not format: # it's also not rgb or hsl
                                    brackets_reg = sublime.Region(brackets_sel.a - 4, brackets_sel.b)
                                    format = self.recognize_from_region(brackets_reg)
                                    if not format: # we failed at format recognition. Revert selection.
                                        word = False
                                    else:
                                        word = brackets_reg
                                else:
                                    word = brackets_reg
                            else:
                                word = brackets_sel
                        else: # otherwise
                            word = False # Reset word so nothing will be replaced

        # Pick a color
        color = self.run_color_picker(format)

        # If got a string with color
        if color:
            # For each selected region
            for region in original_sel:
                if word:
                    # and replace it with picked color
                    view.replace(edit, word, str(color))
                else:
                    # otherwise just replace selection
                    view.replace(edit, region, str(color))

    def recognize_from_region(self, region):
        string = self.view.substr(region).strip()
        return self.recognize_format(string)

    def recognize_format(self, string):
        if string.startswith('#'):
            return 'cssHEXUpper'
        elif string.startswith('[NSColor colorWithCalibratedRed'):
            return 'nscolorRGB'
        elif string.startswith('[NSColor colorWithCalibratedHue'):
            return 'nscolorHSL'
        elif string.startswith('[UIColor colorWithRed'):
            return 'uicolorRGB'
        elif string.startswith('[UIColor colorWithHue'):
            return 'uicolorHSL'
        elif string.startswith('rgba'):
            return 'cssRGBA255'
        elif string.startswith('hsla'):
            return 'cssHSLA'
        elif string.startswith('rgb'):
            return 'cssRGB255'
        elif string.startswith('hsl'):
            return 'cssHSL'
        else:
            return False

    def run_color_picker(self, format):
        args = str(self.settings.get("path"))
        if not format:
            if self.settings.has("defaultFormat"):
                args += ' --format ' + str(self.settings.get("defaultFormat"))
        else:
            args += ' --format ' + str(format)

        if self.settings.has("magnification") and self.settings.get("magnification") != 0:
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
