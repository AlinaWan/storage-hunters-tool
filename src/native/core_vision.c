// x64 Native Tools Command Prompt for VS 2022 (MSVC):
//     cl /LD core_vision.c /Fe:core_vision.dll
// Depended by core\native_methods.py

#include <windows.h>
#include <stdint.h>
#include <stdlib.h>

// Using dllexport so MSVC exposes the symbol in the DLL
__declspec(dllexport) int __stdcall check_pixel_columns(
    const uint8_t* pixels,
    int height,
    int stride,
    const int* x_offsets,
    const uint8_t* target_bgrs,
    int count,
    int tolerance
) {
    int matches = 0;

    for (int i = 0; i < count; i++) {
        int target_x = x_offsets[i];

        if (target_x < 0 || target_x >= (stride / 4)) {
            continue;
        }

        // Target BGR values for this specific column
        int tb = target_bgrs[i * 3];
        int tg = target_bgrs[i * 3 + 1];
        int tr = target_bgrs[i * 3 + 2];

        for (int y = 0; y < height; y++) {
            // Calculate pointer to this pixel: (y * stride) + (x * 4 bytes per pixel)
            const uint8_t* p = pixels + (y * stride) + (target_x * 4);

            // Using abs() logic for tolerance
            if (abs((int)p[0] - tb) <= tolerance &&
                abs((int)p[1] - tg) <= tolerance &&
                abs((int)p[2] - tr) <= tolerance) {
                matches++;
                break; // Move to the next column
            }
        }
    }

    return matches;
}