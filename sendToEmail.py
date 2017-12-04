#!/usr/bin/env python3

####################################
############# paramters ############
####################################

ADDR = 'raspitajse@gmail.com'
PASS = 'neznampass'
SUBJ = 'Datoteke s RaspitajSe radionice'
BODY = 'ovo je automatska poruka poslana skriptom s radionice Istrazivackog centra mladih'
#FILE = ['sendToEmail.py']

####################################
### DO NOT EDIT BELOW THIS LINE ####
####################################

# imports
import smtplib
import mimetypes
import email
import email.mime.application
import email.mime.multipart
import email.mime.text
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import *


############## GUI ###############

class App:
    def __init__(self, root):
        self.filedict = []
        
        self.root = root
        root.title("send files to email")

        self.label = Label(root, text="enter your email address:")
        self.label.grid(row=0, column=0, columnspan=2)

        self.email = Entry(root)
        self.email.grid(row=0, column=2, columnspan=2)
        self.email['width'] = 35

        scrollbarY = Scrollbar(root, orient=VERTICAL)
        self.filelist = Listbox(root, height = 0, yscrollcommand=scrollbarY.set)
        #self.filelist.bind('<<ListboxSelect>>', self.onselect)
        self.filelist.bind('<Double-1>', self.deleteitem)
        
        scrollbarY.config(command=self.filelist.yview)
        #scrollbarY.grid(row=5, column=0)
        self.filelist.grid(row=1, column=0, columnspan=4)
        #self.filelist['state'] = "disabled"
        self.filelist['selectmode'] = BROWSE
        self.filelist['width'] = 58
        self.filelist['height'] = 1
        self.filelist.grid_remove()

        
        
        #self.email['height'] = 10

        self.choose_button = Button(root, text="choose files", command=self.choose)
        self.choose_button.grid(row=2, column=0)

        self.close_button = Button(root, text="close", command=self.exit)
        self.close_button.grid(row=2, column=1)

        self.delete_button = Button(root, text="delete item", command=self.delete_file)
        self.delete_button.grid(row=2, column=2)

        self.send_button = Button(root, text="send all!", command=self.send_files)
        self.send_button.grid(row=2, column=3)

        self.filelist.grid_remove()
        self.send_button.grid_remove()
        self.delete_button.grid_remove()

    def delete_file(self):
        sel = self.filelist.curselection()

        if len(sel) < 1:
            return

        index = sel[0]

        self.filedict.pop(index)
        self.filelist.delete(index)

        if len(self.filedict) > 0:
            self.filelist.grid(row=1, column=0, columnspan=4)
            self.send_button.grid(row=2, column=3)
            self.delete_button.grid(row=2, column=2)
            self.filelist['height'] = min(len(self.filedict), 30)
        else:
            self.filelist.grid_remove()
            self.send_button.grid_remove()
            self.delete_button.grid_remove()

    def check_email():
        pass # TODO

    def send_files(self):

        self.send_button.grid_remove()
        self.delete_button.grid_remove()
        self.choose_button.grid_remove()

        self.close_button.grid(row=2, column=0, columnspan=4)
        
        self.filelist['state'] = "disabled"
        self.email['state'] = "disabled"

        try:
            FILE = self.filedict
            DEST = self.email.get().strip()
            
            # message forming
            msg = email.mime.multipart.MIMEMultipart()
            msg['Subject'] = SUBJ
            msg['From'] = ADDR
            msg['To'] = DEST

            # body forming
            body = email.mime.text.MIMEText(BODY)
            msg.attach(body)

            # file I/O
            if type(FILE) != list and type(FILE) != tuple:
                FILE = [FILE]

            for filename in FILE:
                with open(filename, 'rb') as fp:
                    content = fp.read()
                    att = email.mime.application.MIMEApplication(content, _subtype=filename.split('.')[-1])
                    att.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(att)

            # authentication and sending
            s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            s.login(ADDR, PASS)
            s.sendmail(ADDR, [DEST], msg.as_string())
            s.quit()
            print('[email sent]')
            
            
            showinfo("yeah!", "email sent!")
        except IOError:
            showerror('whoops', 'something went wrong. email was not sent!')
        
    
    def deleteitem(self, evt):
        print('del')
        w = evt.widget
        index = int(w.curselection()[0])

        print(index)
        #print(w.get(index))
        print(self.filedict[index])

        self.filedict.pop(index)
        self.filelist.delete(index)

        if len(self.filedict) > 0:
            self.filelist.grid(row=1, column=0, columnspan=4)
            self.send_button.grid(row=2, column=3)
            self.delete_button.grid(row=2, column=2)
            self.filelist['height'] = min(len(self.filedict), 30)
        else:
            self.filelist.grid_remove()
            self.send_button.grid_remove()
            self.delete_button.grid_remove()

    def onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])

        print(index)
        print(self.filedict[index])

    def choose(self):
        filenames =  filedialog.askopenfilenames(initialdir = "/home/pi/Desktop/radionica",
                                                title = "choose your files")

        for file in filenames:

            if file in self.filedict: continue
            
            file_short = file.split('/')[-1]
            self.filelist.insert(END, file_short)
            self.filedict.append(file)

        if len(self.filedict) > 0:
            self.filelist.grid(row=1, column=0, columnspan=4)
            self.send_button.grid(row=2, column=3)
            self.delete_button.grid(row=2, column=2)
            self.filelist['height'] = min(len(self.filedict), 30)
        else:
            self.filelist.grid_remove()
            self.send_button.grid_remove()
            self.delete_button.grid_remove()
        
    def exit(self):
        exit(0)


if __name__ == '__main__':
    root = Tk()
    my_gui = App(root)
    root.mainloop()


