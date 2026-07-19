REM DxgiCapture.dll
cl /nologo /LD /O2 /Oi /Ot /GL /arch:AVX2 /fp:fast /GS- /Fosrc\native\ /Fdsrc\native\DxgiCapture.pdb src\native\DxgiCapture.cpp /link /LTCG /OPT:REF /OPT:ICF /OUT:src\native\DxgiCapture.dll /IMPLIB:src\native\DxgiCapture.lib

REM MessageBoxWorker.exe
cl /nologo /O2 /Oi /Oy /MT /EHsc /GS- /DNDEBUG /Fesrc\native\MessageBoxWorker.exe /Fosrc\native\ src\native\MessageBoxWorker.cpp /link /OPT:REF /OPT:ICF /SUBSYSTEM:CONSOLE user32.lib /ENTRY:WinMainCRTStartup
