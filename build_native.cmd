@echo off
echo [96m######################################### Initializing environment ##########################################[0m
for %%E in (Community Professional Enterprise BuildTools) do (
    for %%V in (18 2022) do (
        if exist "%ProgramFiles%\Microsoft Visual Studio\%%V\%%E\VC\Auxiliary\Build\vcvars64.bat" (
            call "%ProgramFiles%\Microsoft Visual Studio\%%V\%%E\VC\Auxiliary\Build\vcvars64.bat"
            goto :vcvars64_found
        )
    )
)
echo [31m!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Could not find vcvars64.bat !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![0m
exit /b 1

:vcvars64_found
echo [92m########################################## Environment initialized ##########################################[0m
echo [96m########################################### Starting engine build ###########################################[0m
@echo on
call build_engine_native.cmd
@echo off
echo [92m################################################ Engine done ################################################[0m
echo [96m########################################### Starting local build ############################################[0m
@echo on
call build_local_native.cmd
@echo off
echo [92m################################################ Local done #################################################[0m