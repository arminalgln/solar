import tkinter
# import tkinter

top = tkinter.Tk()

def helloCallBack():
   tkinter.messagebox.showinfo('Hello!','Hello Armin')


B = tkinter.Button(top, text ="Hello", command = helloCallBack)

B.pack()
top.mainloop()