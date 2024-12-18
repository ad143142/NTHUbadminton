import tkinter as tk


def open_form():
    # Top level window
    frame = tk.Tk()
    frame.title("TextBox Input")
    frame.geometry('400x200')

    # Function for getting Input
    # from textbox and printing it
    # at label widget

    def submitBtnFunc(self):
        global account, password
        account = inputacc.get(1.0, "end-1c")
        password = inputpass.get(1.0, "end-1c")
        # quit the window
        frame.quit()

    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        event.widget.tk_focusNext().focus()
        return ("break")

    # TextBox Creation
    textacc = tk.Label(frame, text="Account")
    inputacc = tk.Text(frame, height=5, width=20)
    textpass = tk.Label(frame, text="Password")
    inputpass = tk.Text(frame, height=5, width=20)
    submitBtn = tk.Button(frame, text="Submmit", command=submitBtnFunc)

    inputacc.bind("<Tab>", focus_next_widget)
    submitBtn.bind('<Return>', submitBtnFunc)
    inputpass.bind('<Return>', submitBtnFunc)

    textacc.pack()
    inputacc.pack()
    textpass.pack()
    inputpass.pack()
    submitBtn.pack()

    # Label Creation
    frame.mainloop()
    frame.destroy()
    return account, password
