REM DxgiCapture.dll
cl /LD /O2 /Oi /Ot /GL /arch:AVX2 /fp:fast /GS- /Fosrc\native\ /Fdsrc\native\DxgiCapture.pdb src\native\DxgiCapture.cpp /link /LTCG /OPT:REF /OPT:ICF /OUT:src\native\DxgiCapture.dll /IMPLIB:src\native\DxgiCapture.lib

REM MessageBoxWorker.exe
cl /O2 /Oi /Oy /MT /EHsc /GS- /DNDEBUG /Fesrc\native\MessageBoxWorker.exe /Fosrc\native\ src\native\MessageBoxWorker.cpp /link /OPT:REF /OPT:ICF /SUBSYSTEM:CONSOLE user32.lib /ENTRY:WinMainCRTStartup

REM stvision.dll
ml64 /c /Fosrc\native\threshold.obj src\native\threshold.asm
link /DLL /NOENTRY src\native\threshold.obj /DEF:src\native\stvision.def /OUT:src\native\stvision.dll /IMPLIB:src\native\stvision.lib