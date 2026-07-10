option casemap:none

PUBLIC find_line_bounds
.code

; uint32_t find_line_bounds(uint8_t* mask_buffer, int width, int height, uint32_t* result_coords);
; Returns 1 if line found, 0 otherwise.
find_line_bounds PROC
    ; Save non-volatile registers per ABI requirements
    push rbx
    push r12
    push r13
    push r14

    mov rbx, rcx        ; mask_buffer
    mov r10d, -1        ; min_x (initialized to -1 / 0xFFFFFFFF)
    mov r11d, 0         ; max_x (initialized to 0)
    
    xor r12, r12        ; col_idx (0)
col_loop:
    xor r13, r13        ; row_idx (0)
    mov r14, r12        ; current_ptr_offset = col_idx

row_loop:
    ; Check if pixel is non-zero
    cmp byte ptr [rbx + r14], 0
    jne found_pixel
    
    add r14, rdx        ; next row: offset += width
    inc r13
    cmp r13, r8         ; if row < height, continue
    jl row_loop
    
    ; If we finished the row_loop without finding a pixel in this column:
    ; Optimization: If we already found the line, and this empty column is
    ; after the max_x, we can terminate early.
    cmp r10d, -1
    jne check_termination
    jmp next_column

found_pixel:
    ; Update min_x if this is the first pixel found
    cmp r10d, -1
    cmove r10d, r12d
    ; Always update max_x to current column
    mov r11d, r12d

next_column:
    inc r12
    cmp r12, rdx        ; if col < width, continue
    jl col_loop
    jmp done

check_termination:
    ; Once we've found the line, the first empty column after the line
    ; signifies we've finished the cluster.
    jmp done

done:
    ; Check if we found anything
    cmp r10d, -1
    je not_found
    
    ; Save results to result_coords (R9)
    mov [r9], r10d      ; x1
    mov [r9+4], r11d    ; x2
    mov eax, 1          ; return success
    jmp finish

not_found:
    mov eax, 0

finish:
    ; Restore non-volatile registers
    pop r14
    pop r13
    pop r12
    pop rbx
    ret
find_line_bounds ENDP
END