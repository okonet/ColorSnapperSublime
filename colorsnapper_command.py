import sublime
import sublime_plugin
import subprocess

class PickWithColorSnapperCommand(sublime_plugin.TextCommand):
    """
    Runs ColorSnapper external application and replaces
    selected text with a picked color code.
    Attpemts to automatically recognize CSS format from cursor position
    and replace the whole color code with the same format.
    """

    def run(self, edit):
        view = self.view
        sel = view.sel()
        region_to_replace = sel[0]
        self.settings = sublime.load_settings('ColorSnapper.sublime-settings')
        if self.settings.has("defaultFormat"): format = self.settings.get("defaultFormat")

        # Determine in which format to pick
        if self.settings.get('autoFormat'):
            # If selection contains more than 1 symbol we will not modify it
            # But we will make an exrta check if it's a valid HEX color without #
            # Otherwise defaults from settings will be used.
            if not region_to_replace.empty():
                if self.is_valid_hex_color(view.substr(region_to_replace).strip()):
                    format = 'hex'
            # If selection is empty, we will make our best to recognize format.
            else:
                # Search for color regions according to CSS language grammar.
                regions = self.get_color_regions(view)
                for region in regions:
                    # If cursor is inside one of the color regions,
                    # we'll set a region to a matched color region.
                    if region.contains(sel[0]):
                        region_to_replace = region
                        break

                # We've found a color format match in cursor position...
                if not region_to_replace.empty():
                    # Now determining format. Convert region to string.
                    string = self.view.substr(region).strip()
                    if string.startswith('#'):
                        # If string starts with # it's a CSS HEX format
                        if self.settings.has("upperCaseHEX") and self.settings.get("upperCaseHEX"):
                            format = 'cssHEXUpper'
                        else:
                            format = 'cssHEX'
                    # Otherwise it's an CSS RGB (without rgb prefix)
                    else:
                        format = "rgb"

        # Now pick a color running a shell command
        color = self.run_color_picker(format)

        # Check if we got a color back from ColorSnapper
        if color:
            # For each selected region
            for region in sel:
                if region_to_replace.contains(region):
                    view.replace(edit, region_to_replace, str(color))
                else:
                    view.replace(edit, region, str(color))

    def run_color_picker(self, format):
        args = str(self.settings.get("path"))
        if bool(format): args += ' --format ' + str(format)

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

    def get_color_regions(self, view):
        hex_rgb = view.find_by_selector("constant.other.color.rgb-value.css")
        rbg_percent = view.find_by_selector("constant.other.color.rgb-percentage.css")
        less_colors = view.find_by_selector("constant.other.rgb-value.css")
        return hex_rgb + rbg_percent + less_colors

    def is_valid_hex_color(self, s):
      if len(s) not in (3, 6):
        return False
      try:
        return 0 <= int(s, 16) <= 0xffffff
      except ValueError:
        return False
