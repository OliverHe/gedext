# Gedext
A tool to replace the now defunct "External tools" plugin in Gedit

## Instructions for use
Place the text to be processed in the main area and press a button.

Currently there are four buttons:
* B64 decode: For Base64 decoding
* json: For JSON validation and "beautifying"
* X509: For reading PEM encoded certificates
* XML: For XML validation and "beautifying"

## Versions
* 0.1 - First version for github
* 0.2 - Show version in statusbar, switch to plaintextedit, use other cert for testing

## TODO
1. Cleanup specific x509 output
2. Get the XML working
3. Convert buttons to QAction's
4. Add those actions to a File menu
5. Add a help --> About menu
6. Think about security implications (maybe I should do that sooner)
7. Filter out binary MIME types when decoding base64
8. Handoff binary results after base64 decoding to system
9. Figure out packaging for Windows
10. Figure out packaging for MacOS
11. Expand on Linux packaging
12. Maybe do an RPM?
13. Expand by allowing:
    * Base64 encoding
    * Varying kinds of certificate validation
    * JSON minifying
    * XML minifying
14. Figure out why font seems to ignored sometimes -testing-
15. Split main python file according to function
16. Figure out why title doesn't work in applications overview.

## Packaging

### Linux

#### First run

This is mostly as a reminder to myself

    python3 -m venv packenv
    source packenv/bin/activate
    pip3 install PyQt6 PyInstaller cryptography
    pyinstaller gedext.py
