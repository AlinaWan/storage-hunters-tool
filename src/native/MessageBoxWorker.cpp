#include <windows.h>
#include <iostream>
#include <string>

std::wstring s2ws(const std::string& str) {
    int size_needed = MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), NULL, 0);
    std::wstring wstrTo(size_needed, 0);
    MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), &wstrTo[0], size_needed);
    return wstrTo;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd) {
    if (__argc < 4) return 1;

    std::wstring text = s2ws(__argv[1]);
    std::wstring title = s2ws(__argv[2]);
    UINT flags = static_cast<UINT>(std::stoul(__argv[3]));

    int result = MessageBoxW(NULL, text.c_str(), title.c_str(), flags);

    // send to stdout for python to read
    std::cout << result << std::endl;

    return 0;
}