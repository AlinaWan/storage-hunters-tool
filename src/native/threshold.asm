option casemap:none

PUBLIC threshold

.code

; void threshold(const uint8_t* src, uint8_t* dst, int length, uint8_t threshold);
; RCX = src
; RDX = dst
; R8  = length
; R9B = threshold

threshold PROC

    ; Build threshold vector (threshold ^ 0x80 repeated 16 times)
    movzx eax, r9b
    xor al, 80h

    movd xmm1, eax
    punpcklbw xmm1, xmm1
    punpcklbw xmm1, xmm1
    punpcklwd xmm1, xmm1
    punpckldq xmm1, xmm1

    mov r10, r8          ; Save original length
    shr r8, 4            ; Number of 16-byte blocks
    jz tail_loop

loop_proc:
    movdqu xmm2, [rcx]
    pxor xmm2, xmmword ptr [xor_val]
    pcmpgtb xmm2, xmm1
    pand xmm2, xmmword ptr [mask80]    ; Convert 0xFF -> 0x80
    movdqu [rdx], xmm2

    add rcx, 16
    add rdx, 16
    dec r8
    jnz loop_proc

tail_loop:
    and r10, 0Fh         ; Remaining bytes
    jz done

process_byte:
    mov al, [rcx]
    cmp al, r9b
    seta al
    shl al, 7            ; 0 -> 0x00, 1 -> 0x80
    mov [rdx], al

    inc rcx
    inc rdx
    dec r10
    jnz process_byte

done:
    ret

threshold ENDP

.data
align 16

xor_val db 16 dup(80h)
mask80 db 16 dup(80h)

END