#-------------------------------------------------------------------------------
# Name:        hexcontroller.py
# Purpose:     Sets up and runs GUI application and related functions
#
# Author:      Langston Graham
#
# Created:     08/14/2013
#-------------------------------------------------------------------------------

import hexreader
import hexvisgui
import binvis

if __name__=='__main__':
    app = hexvisgui.gui(None)
    app.mainloop()