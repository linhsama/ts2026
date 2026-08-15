Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\DAI HOC TAY DO\Desktop\ts2026\"
WshShell.Run "pythonw " & Chr(34) & "C:\Users\DAI HOC TAY DO\Desktop\ts2026\server.py" & Chr(34), 0, False
