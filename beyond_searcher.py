import os
import sys
import subprocess

import wx.richtext as rt
import wx
from dndbeyond_websearch import Searcher

class SearcherFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(SearcherFrame, self).__init__(*args, **kw)

        #print(Searcher().search('Otyugh')[0])
        self.setup()
        self.Show()


    def setup(self):
        self.SetBackgroundColour("white")
        self.SetTitle("Beyond Searcher BETA 1")
        self.SetSize(400, 600)
        box = wx.BoxSizer(wx.VERTICAL)
        self.searchbox = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER, id=1)
        self.searchbox.WriteText("Enter Search Query")
        self.Bind(wx.EVT_TEXT_ENTER, self.search, id = 1)
        self.urlbox = rt.RichTextCtrl(self, style= wx.TE_MULTILINE | wx.TE_READONLY)
        self.urlbox.Bind(wx.EVT_TEXT_URL, self.OnURL)
        self.resultbox = rt.RichTextCtrl(self)
        box.Add(self.searchbox, 1, flag=wx.EXPAND | wx.ALL, border = 5)
        box.Add(self.urlbox, 1, flag=wx.EXPAND | wx.ALL, border = 5)
        box.Add(self.resultbox, 7, flag=wx.EXPAND | wx.ALL, border = 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.previousbutton = wx.Button(self, -1, "<<")
        self.previousbutton.Bind(wx.EVT_BUTTON, self.prev)
        self.previousbutton.Disable()
        self.nextbutton = wx.Button(self, -1, ">>")
        self.nextbutton.Bind(wx.EVT_BUTTON, self.next)
        self.nextbutton.Disable()
        hbox.Add(self.previousbutton, 1, flag=wx.EXPAND | wx.ALL)
        hbox.Add(self.nextbutton, 1, flag=wx.EXPAND | wx.ALL)
        box.Add(hbox, 1, flag=wx.EXPAND  | wx.ALL, border = 10)
        self.SetSizer(box)


    def prev(self, event):
        idx = self.results.index(self.result)
        idx -= 1
        if idx < 0:
            idx = len(self.results)-1
        self.show(self.results[idx])

    def next(self, even):
        idx = self.results.index(self.result)
        idx += 1
        if idx >= len(self.results):
            idx = 0
        self.show(self.results[idx])

    def search(self, event):
        query = str(self.searchbox.GetValue())
        self.results = Searcher().search(query)
        if self.results:
            self.show(self.results[0])
            if len(self.results) > 1:
                self.previousbutton.Enable()
                self.nextbutton.Enable()
            else:
                self.previousbutton.Disable()
                self.nextbutton.Disable()
        else:
            self.resultbox.Clear()
            self.resultbox.WriteText(":(")
    
    def show(self, result):
        self.result=result
        rtc = self.resultbox
        rtc.Freeze()
        rtc.Clear()

        rtc.BeginParagraphSpacing(0, 20)  # SPACING
 
        rtc.BeginAlignment(wx.TEXT_ALIGNMENT_CENTRE) # ALIGNMENT
        rtc.BeginBold()  # BOLD

        rtc.BeginFontSize(14) # FONT SIZE
        rtc.WriteText(result.title)
        rtc.EndFontSize() # END FONT SIZE
        rtc.Newline()

        rtc.BeginItalic()  # ITALIC
        rtc.WriteText(result.breadcrumbs)
        rtc.EndItalic()  # END ITALIC

        rtc.Newline()
        rtc.EndBold() # END BOLD

        urlStyle = rt.RichTextAttr()
        urlStyle.SetTextColour(wx.BLUE)
        urlStyle.SetFontUnderlined(True)

        self.urlbox.Clear()
        self.urlbox.BeginStyle(urlStyle)  # URL STYLE
        self.urlbox.BeginURL(result.url) # URL
        self.urlbox.WriteText(result.url)
        self.urlbox.EndURL()  # END URL
        self.urlbox.EndStyle()  # END URL STYLE
        
        rtc.EndAlignment()  # END ALIGNMENT
        rtc.Newline()

        text = " ... ".join(result.snippets)
        rtc.WriteText(text)
        rtc.EndParagraphSpacing() # END SPACING
        rtc.Thaw()

    def OnURL(self, event):
        url = self.result.url
        if sys.platform=='win32':
            os.startfile(url)
        elif sys.platform=='darwin':
            subprocess.Popen(['open', url])
        else:
            try:
                subprocess.Popen(['xdg-open', url])
            except OSError:
                print 'Please open a browser on: '+url

    def OnExit(self, event):
        self.Close(True)


if __name__ == '__main__':
    app = wx.App()
    frm = SearcherFrame(None)
    app.MainLoop()

