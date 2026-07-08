Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
Root = FSO.GetParentFolderName(WScript.ScriptFullName)
cmd = "cmd.exe /k cd /d """ & Root & """ && run.bat"
WshShell.Run cmd, 1, False
