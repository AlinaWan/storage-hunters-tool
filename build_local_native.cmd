REM stvision.dll
ml64 /nologo /c /Fosrc\native\threshold.obj src\native\threshold.asm
ml64 /nologo /c /Fosrc\native\find_line_bounds.obj src\native\find_line_bounds.asm
link /nologo /DLL /NOENTRY src\native\threshold.obj src\native\find_line_bounds.obj /DEF:src\native\stvision.def /OUT:src\native\stvision.dll /IMPLIB:src\native\stvision.lib