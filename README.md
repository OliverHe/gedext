# Gedext
A tool to replace the now defunct "External tools" plugin in Gedit. 

First there was xmllint to prettyprint the long lines of xml found
in logging when troubleshooting issues. Later came json, so jq was
added to the toolbox. When I found that Gedit supported External tools
I created shortcuts in gedit that could call xmllint or jq to do the
reformatting in a convenient text-editor.
As time passed more tools were added, even if it became a bit hacky.

Then Gedit decided that the external tools code was unmaintainable and
it was unceremoniously dropped. Which led to a POLA violation some time
after upgrading to Fedora 42.

Having tinkered with Python before I decided to write a replacement
from scratch. The first attempt was made in Gnome Builder, but after
getting stuck there I remembered tinkering with QT(3?) as well, so I
switched to PyCharm and PyQt6 which has the added benefit that it should
work on Linux, Windows and macOS alike.


## Instructions for use
Place the text to be processed in the main area and press a button.

Currently there are four buttons:
* B64 decode: For Base64 decoding
* json: For JSON validation and "beautifying"
* X509: For reading PEM encoded certificates
* XML: For XML validation and "beautifying"
* Clear: For clearing all content

## Versions
* 0.1 - First version for github
* 0.2 - Show version in statusbar, switch to plaintextedit, use other cert for testing
* 0.3 - Use different file for about dialog which also necessitates a globals file.
* 0.4 - Expand about dialog, use minidom for xml prettyprinting.
* 0.5 - Add actions including a timestamp insert.

## TODO
1. Cleanup specific x509 output
2. Convert buttons to QAction's
3. Add those actions to a File menu
4. Think about security implications (maybe I should do that sooner)
5. Filter out binary MIME types when decoding base64
6. Handoff binary results after base64 decoding to system
7. Figure out packaging for Linux
8. Figure out packaging for Windows
9. Figure out packaging for MacOS
10. Expand by allowing:
    * Base64 encoding
    * Varying kinds of certificate validation
    * JSON minifying
    * XML minifying
12. Split main python file according to function
13. Figure out why title doesn't work in applications overview.
14. See if I can apply the conversion only on selected text.
15. Wonder about replacing minidom with lxml

## Packaging
These are mostly as a reminder to myself
### Linux
#### First run

    python3 -m venv packenv
    source packenv/bin/activate
    pip3 install PyQt6 PyInstaller cryptography
    pyinstaller --onefile gedext.py

### Windows
#### First run
* Install Git for Windows
* Install Python as admin and added to PATH

Use Git Bash as follows:

    python -m venv packenv
    . packenv/Scripts/Activate
    Pyinstaller.exe --onefile --noconsole gedext.py