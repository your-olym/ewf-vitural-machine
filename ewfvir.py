#! /usr/bin/env python
from tkinter import *
import os
import subprocess
from pykeyboard import *
import time
 
ke=PyKeyboard()
tk=Tk()
content = StringVar()
comm=Entry(tk,textvariable=content)
comm.pack()
content.set("4.E01")


content2 = StringVar()
comm2=Entry(tk,textvariable=content2)
comm2.pack()
content2.set("mpoint")


global fil,pat

def getfil():
        global fil
        fil=comm.get()
        return(fil)

def getpat():
        global pat
        pat=comm2.get()
        return(pat)
def processewf():
        tfil=getfil()
        tpat=getpat()
        os.system('open /Applications/iterm.app')
        time.sleep(3)
        ke.type_string("\n"+'clear'+'\n')
        time.sleep(2)
        ke.type_string("mkdir ~/tmp mkdir ~/tmp/"+tpat+'\n')
        time.sleep(1)
        ke.type_string("ewfmount -X volicon=/Library/Filesystems/osxfuse.fs/Contents/Resources/Volume.icns  /Users/dsa/Downloads/"+tfil+" ~/tmp/"+tpat)


        print("mount success")#点击之后会在idle中显示

def processvmdk():
        tfil=getfil()
        tpat=getpat()
        os.system('open /Applications/iterm.app')
        time.sleep(5)
        ke.type_string("hdiutil attach -imagekey diskimage-class=CRawDiskImage -nomount ~/tmp/"+tpat+"/ewf1\n")
        time.sleep(2)
        ke.type_string('/usr/local/Cellar/qemu/6.1.0_1/bin/qemu-img convert -p -O vmdk ~/tmp/'+tpat+'/ewf1 /Users/dsa/Virtual\ Machines.localized/mpoint.vmwarevm/'+tfil+'.vmdk')



def shand():
        
        time.sleep(3)
        ke.type_string("cd /etc/sysconfig/network-scripts/\n")
        time.sleep(1)
        ke.type_string("vi ifcfg-en\t\n")


def main():

        comm.pack()
        
        btnssh=Button(tk,text="ewfmount",fg="red",command=processewf).pack()#文本，字体颜色，和点击评论，并没有标定具体位置，
        btnvm=Button(tk,text="creat vmdk ",bg="yellow",command=processvmdk).pack()
        btns=Button(tk,text="shell",bg="yellow",command=shand).pack()
        

        tk.mainloop()

if __name__=="__main__":
        main()
