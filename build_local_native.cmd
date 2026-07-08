REM stvision.dll
ml64 /c /Fosrc\native\threshold.obj src\native\threshold.asm
link /DLL /NOENTRY src\native\threshold.obj /DEF:src\native\stvision.def /OUT:src\native\stvision.dll /IMPLIB:src\native\stvision.lib