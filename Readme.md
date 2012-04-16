About
=====

A Sublime Text 2 plugin for picking colors using ColorSnapper app (http://colorsnapper.com).

Requirements:

* Mac with Mac OS X 10.6+
* ColorSnapper 1.0.7+ (buy from Mac App Store: http://itunes.apple.com/app/colorsnapper/id418176775?mt=12)

Installation
============

You can install this package by running the following in your `Packages`:

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
    git clone git://github.com/okonet/ColorSnapperSublime.git ColorSnapper

Options
=======

Settings are located in ColorSnapper.sublime-settings inside plugin directory and include:

* path -- Path to ColorSnapper executable. Usually it shouldn't be changed from default.
* autoFormat -- if true, plugin will attempt to get a correct format from selection and use it for picked color
* format -- Default format to fall back if it wasn't recognized from selection. Remove to use ColorSnapper app settings
* magnification -- Magnification level of picker. Remove to use ColorSnapper app settings

License
=======

All of ColorSnapper plugin is licensed under the MIT license.

Copyright (c) 2012 Andrey Okonechnikov (http://okonet.ru)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
