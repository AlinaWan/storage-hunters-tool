#include <windows.h>
#include <d3d11.h>
#include <dxgi1_2.h>
#include <wrl/client.h>
#include <memory>

#pragma comment(lib, "d3d11.lib")
#pragma comment(lib, "dxgi.lib")

using Microsoft::WRL::ComPtr;

struct DXGIContext {
    ComPtr<ID3D11Device> device;
    ComPtr<ID3D11DeviceContext> context;
    ComPtr<IDXGIOutputDuplication> deskDupl;
    ComPtr<ID3D11Texture2D> stagingTexture;
    UINT stagingWidth = 0;
    UINT stagingHeight = 0;

    // Track the dimensions of the last output to validate regions
    DXGI_OUTPUT_DESC outputDesc = {};
};

void ResetDuplication(DXGIContext* ctx) {
    if (ctx) {
        ctx->stagingTexture.Reset();
        ctx->deskDupl.Reset();
        ctx->stagingWidth = 0;
        ctx->stagingHeight = 0;
    }
}

bool InitializePipeline(DXGIContext* ctx) {
    ResetDuplication(ctx);

    if (!ctx->device) {
        UINT flags = D3D11_CREATE_DEVICE_BGRA_SUPPORT;
#ifdef _DEBUG
        flags |= D3D11_CREATE_DEVICE_DEBUG;
#endif
        D3D_FEATURE_LEVEL featureLevels[] = { D3D_FEATURE_LEVEL_11_1, D3D_FEATURE_LEVEL_11_0 };

        HRESULT hr = D3D11CreateDevice(nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, flags,
            featureLevels, ARRAYSIZE(featureLevels), D3D11_SDK_VERSION,
            &ctx->device, nullptr, &ctx->context);
        if (FAILED(hr)) return false;
    }

    ComPtr<IDXGIDevice> dxgiDevice;
    if (FAILED(ctx->device.As(&dxgiDevice))) return false;

    ComPtr<IDXGIAdapter> dxgiAdapter;
    if (FAILED(dxgiDevice->GetParent(__uuidof(IDXGIAdapter), reinterpret_cast<void**>(dxgiAdapter.GetAddressOf())))) return false;

    ComPtr<IDXGIOutput> dxgiOutput;
    if (FAILED(dxgiAdapter->EnumOutputs(0, &dxgiOutput))) return false;

    // Store descriptor for region bounding validation
    dxgiOutput->GetDesc(&ctx->outputDesc);

    ComPtr<IDXGIOutput1> dxgiOutput1;
    if (FAILED(dxgiOutput.As(&dxgiOutput1))) return false;

    if (FAILED(dxgiOutput1->DuplicateOutput(ctx->device.Get(), &ctx->deskDupl))) {
        ResetDuplication(ctx);
        return false;
    }

    return true;
}

bool EnsureStagingTexture(DXGIContext* ctx, UINT width, UINT height) {
    if (ctx->stagingTexture && ctx->stagingWidth == width && ctx->stagingHeight == height) {
        return true;
    }

    D3D11_TEXTURE2D_DESC desc = {};
    desc.Width = width;
    desc.Height = height;
    desc.MipLevels = 1;
    desc.ArraySize = 1;
    desc.Format = DXGI_FORMAT_B8G8R8A8_UNORM;
    desc.SampleDesc.Count = 1;
    desc.Usage = D3D11_USAGE_STAGING;
    desc.CPUAccessFlags = D3D11_CPU_ACCESS_READ;

    ctx->stagingTexture.Reset();
    if (FAILED(ctx->device->CreateTexture2D(&desc, nullptr, &ctx->stagingTexture))) return false;

    ctx->stagingWidth = width;
    ctx->stagingHeight = height;
    return true;
}

extern "C" {
    __declspec(dllexport) DXGIContext* __cdecl InitContext() {
        auto ctx = std::make_unique<DXGIContext>();
        InitializePipeline(ctx.get());
        return ctx.release();
    }

    // Returns a raw CPU pointer to the mapped memory and the RowPitch required by NumPy
    __declspec(dllexport) unsigned char* __cdecl GrabFramePointer(DXGIContext* ctx, int left, int top, int right, int bottom, int* outRowPitch) {
        if (!ctx) return nullptr;

        if (!ctx->deskDupl && !InitializePipeline(ctx)) {
            return nullptr;
        }

        // 1. Sanity check bounds validation
        int max_width = ctx->outputDesc.DesktopCoordinates.right - ctx->outputDesc.DesktopCoordinates.left;
        int max_height = ctx->outputDesc.DesktopCoordinates.bottom - ctx->outputDesc.DesktopCoordinates.top;
        if (left < 0 || top < 0 || right <= left || bottom <= top || right > max_width || bottom > max_height) {
            return nullptr;
        }

        ComPtr<IDXGIResource> desktopResource;
        DXGI_OUTDUPL_FRAME_INFO frameInfo;

        // Short timeout for high throughput frame requests
        HRESULT hr = ctx->deskDupl->AcquireNextFrame(16, &frameInfo, &desktopResource);

        if (hr == DXGI_ERROR_ACCESS_LOST || hr == DXGI_ERROR_DEVICE_REMOVED || hr == DXGI_ERROR_DEVICE_RESET || hr == DXGI_ERROR_INVALID_CALL) {
            if (hr == DXGI_ERROR_DEVICE_REMOVED || hr == DXGI_ERROR_DEVICE_RESET) {
                ctx->device.Reset();
            }
            ResetDuplication(ctx);
            return nullptr;
        }

        if (FAILED(hr)) return nullptr; // Timeout or general error

        ComPtr<ID3D11Texture2D> frameTexture;
        if (FAILED(desktopResource.As(&frameTexture))) {
            ctx->deskDupl->ReleaseFrame();
            return nullptr;
        }

        UINT targetWidth = right - left;
        UINT targetHeight = bottom - top;

        if (!EnsureStagingTexture(ctx, targetWidth, targetHeight)) {
            ctx->deskDupl->ReleaseFrame();
            return nullptr;
        }

        D3D11_BOX sourceBox = { (UINT)left, (UINT)top, 0, (UINT)right, (UINT)bottom, 1 };
        ctx->context->CopySubresourceRegion(ctx->stagingTexture.Get(), 0, 0, 0, 0, frameTexture.Get(), 0, &sourceBox);

        // #3 Flush command queue to guarantee immediate execution before Map
        ctx->context->Flush();

        D3D11_MAPPED_SUBRESOURCE mappedResource;
        hr = ctx->context->Map(ctx->stagingTexture.Get(), 0, D3D11_MAP_READ, 0, &mappedResource);

        // Immediate release of desktop frame loop execution right after copying on GPU
        ctx->deskDupl->ReleaseFrame();

        if (SUCCEEDED(hr)) {
            *outRowPitch = mappedResource.RowPitch;
            return reinterpret_cast<unsigned char*>(mappedResource.pData);
        }

        return nullptr;
    }

    __declspec(dllexport) void __cdecl UnlockFramePointer(DXGIContext* ctx) {
        if (ctx && ctx->stagingTexture) {
            ctx->context->Unmap(ctx->stagingTexture.Get(), 0);
        }
    }

    __declspec(dllexport) void __cdecl CloseContext(DXGIContext* ctx) {
        if (ctx) {
            ResetDuplication(ctx);
            ctx->context.Reset();
            ctx->device.Reset();
            delete ctx;
        }
    }
}