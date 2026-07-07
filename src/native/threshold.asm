option casemap:none

PUBLIC threshold

.code

; void threshold(const uint8_t* src, uint8_t* dst, int length, uint8_t threshold);
threshold PROC
    ; threshold vector (threshold ^ 0x80)
    movzx eax, r9b
    xor al, 80h
    
    ; broadcast the threshold to XMM1
    movd xmm1, eax
    punpcklbw xmm1, xmm1
    punpcklbw xmm1, xmm1
    punpcklwd xmm1, xmm1
    punpckldq xmm1, xmm1

    ; generate the 0x80 constant in XMM3 for reuse
    pcmpeqd xmm3, xmm3     ; xmm3 = 0xFF...FF
    psllw   xmm3, 7        ; xmm3 = 0x8080...80 (16 bytes of 0x80)

    mov r10, r8          ; Save original length
    shr r8, 4            ; Number of 16-byte blocks
    jz tail_loop

loop_proc:
    movdqu xmm2, [rcx]     ; Load 16 bytes
    pxor    xmm2, xmm3
    pcmpgtb xmm2, xmm1
    pand    xmm2, xmm3
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
END
