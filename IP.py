#!/usr/bin/env python3

import tkinter
from tkinter import messagebox
import subprocess

def get_ip():
    args = ['hostname', '-I']
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    shell=False)

    out = process.stdout.read().decode('utf-8')
    
    return out.replace(' ', '\n').strip()

# works only on UNIX. For now...
system_cmd = 'hostname -I | sed -r "s/([^\s]*)(\s+)([^\s*])/\1\n\3/g"'

# hide main window
root = tkinter.Tk()
root.option_add('*Dialog.msg.width', 15)
root.withdraw()



messagebox.showinfo("local IP", get_ip())



