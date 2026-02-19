#pNotes
#Copyright (C) 2026 TheProjectDark
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

import wx

class Frame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="pNotes")
        self.SetClientSize(self.FromDIP((800, 600)))

        panel = wx.Panel(self)

        menubar = wx.MenuBar()
        menuHelp = wx.Menu()
        itemAbout = menuHelp.Append(wx.ID_ABOUT, "&About")
        menubar.Append(menuHelp, "&Help")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnAbout, itemAbout)

        vboxMain = wx.BoxSizer(wx.VERTICAL)
        vboxTop = wx.BoxSizer(wx.HORIZONTAL)

        self.save_button = wx.Button(panel, label="Save")
        self.open_button = wx.Button(panel, label="Open")

        self.save_button.Bind(wx.EVT_BUTTON, self.OnSave)
        self.open_button.Bind(wx.EVT_BUTTON, self.OnOpen)

        vboxTop.Add(self.save_button, 0, wx.ALL, self.FromDIP(5))
        vboxTop.Add(self.open_button, 0, wx.ALL, self.FromDIP(5))
        vboxTop.AddStretchSpacer()

        self.field = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.field.Bind(wx.EVT_CHAR_HOOK, self.OnCharHook)

        vboxMain.Add(vboxTop, 0, wx.EXPAND)
        vboxMain.Add(self.field, 1, wx.EXPAND | wx.ALL, self.FromDIP(5))

        panel.SetSizer(vboxMain)

        self.Centre()
        self.Show()

    #Functions/Logic
    def OnCharHook(self, event):#Tab
        if event.GetKeyCode() == wx.WXK_TAB:
            frm, to = self.field.GetSelection()
            self.field.Replace(frm, to, "    ")
            self.field.SetInsertionPoint(frm + 4)
            return
        event.Skip()

    def OnSave(self, event):
        with wx.FileDialog(
            self,
            "Save file",
            wildcard="Text files (*.txt)|*.txt|All files (*.*)|*.*",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            path = fileDialog.GetPath()

            try:
                with open(path, "w") as file:
                    file.write(self.field.GetValue())
                    wx.MessageBox("File saved successfully", "Saving", wx.OK | wx.ICON_INFORMATION)
            except IOError:
                wx.LogError(f"Could not save file: {path}")
                    

    def OnOpen(self, event):
        with wx.FileDialog(
            self,
            "Open file",
                wildcard="Text files (*.txt)|*.txt|All files (*.*)|*.*",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            try:
                with open(path, "r") as file:
                    self.field.SetValue(file.read())
            except IOError:
                wx.LogError(f"Could not open file: {path}")

    def OnAbout(self, event):
        wx.MessageBox(
            "pNotes\nwxPython",
            "About",
            wx.OK | wx.ICON_INFORMATION
        )

class App(wx.App):
    def OnInit(self):
        Frame()
        return True

app = App()
app.MainLoop()