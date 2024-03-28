# ==============================================================================
#
# TKinter based Table class which accepts any other tkinter widgets as cells
#
# Includes scrollbar to scroll through the table
#
# ==============================================================================

import tkinter as tk
from tkinter import ttk
from tkinter import N, S, E, W, NSEW

class Table(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(self)
        self.canvas.grid(column=0, row=0, sticky=(N,S,E,W))

        self.frame = ttk.Frame(self.canvas)
        self.frame.grid(column=0, row=0, sticky=(N,S,E,W))

        self.scrollbar = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar.grid(column=1, row=0, sticky=(N,S))
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.myWindow = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.frame.bind('<Configure>', self._configure_frame)
        self.canvas.bind('<Configure>', self._configure_canvas)

    def setHeaders(self, headers):
        for i, header in enumerate(headers):
            label = ttk.Label(self.frame, text=header)
            label.grid(row=0, column=i, sticky=NSEW, padx=(2, 2), pady=(2, 2))

    # track changes to the canvas and frame width and sync them, also updating the scrollbar
    def _configure_frame(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.frame.winfo_reqwidth(), self.frame.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.frame.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.frame.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.frame.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.myWindow, width=self.canvas.winfo_width())

# main driver
if __name__ == "__main__":
    app = tk.Tk()
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)
    
    table = Table(app)
    table.grid(row=0, column=0, sticky=NSEW)
    table.setHeaders(["Header 0.1", "Header 0.2", "Header 0.3", "Header 0.4", "Header 0.5", "Header 0.6", "Header 0.7", "Header 0.8"])

    image = tk.PhotoImage(file="./test.png")

    for y in range(1, 50):
        for x in range(8):
            match x:
                case 0:
                    myWidget = ttk.Entry(table.frame, width = 20, )
                    myWidget.insert(0,f"Entry {y}.{x}")
                case 1:
                    myWidget = ttk.Checkbutton(table.frame, width = 15, text=f"Checkbox {y}.{x}")
                case 2:
                    myWidget = ttk.Label(table.frame, compound=tk.LEFT, text=f"ImageLabel {y}.{x}", image=image)
                case 3:
                  myWidget = ttk.Radiobutton(table.frame, text=f"Radio {y}.{x}", value={y})
                case 4:
                    vlist = ["Option1", "Option2", "Option3", "Option4", "Option5"]
                    myWidget = ttk.Combobox(table.frame, text=f"Combobox {y}.{x}", values = vlist)
                case 5:
                    myWidget = ttk.Button(table.frame, text=f"Button {y}.{x}")
                case 6:
                    myWidget = ttk.Scale(table.frame, orient=tk.HORIZONTAL)
                case 7:
                    myWidget = ttk.Progressbar(table.frame, orient='horizontal', mode='determinate', length=100)
                case _:
                    myWidget = ttk.Label(table.frame, text=f"Label {y}.{x}")

            table.frame.rowconfigure(y, weight=1)
            table.frame.columnconfigure(x, weight=1)
            myWidget.grid(row=y, column=x, sticky=NSEW)

    app.mainloop()