assume cs:code,ds:data,ss:stack,es:extended

extended segment
	db 1024 dup (0)
extended ends

stack segment
	db 1024 dup (0)
stack ends

data segment
	_buff_p db 256 dup (24h)
	_buff_s db 256 dup (0)
	_msg_p db 0ah,'Output:',0
	_msg_s db 0ah,'Input:',0
	_a dw 0
	_i dw 0
	_sum dw 0
	_N dw 0
data ends

code segment
start:	mov ax,extended
	mov es,ax
	mov ax,stack
	mov ss,ax
	mov sp,1024
	mov bp,sp
	mov ax,data
	mov ds,ax

_1:	MOV AX,1
	MOV DS:[_a],AX
_2:	MOV AX,1
	MOV DS:[_i],AX
_3:	MOV AX,0
	MOV DS:[_sum],AX
_4:	CALL _READ
	MOV ES:[0],AX
_5:	MOV AX,ES:[0]
	MOV DS:[_N],AX
_6:	MOV DX,1
	MOV AX,DS:[_I]
	CMP AX,DS:[_N]
	JB _6_N
	MOV DX,0
_6_N:	MOV ES:[2],DX
_7:	MOV AX,ES:[2]
	CMP AX,0
	JNE _7_N
	JMP FAR PTR _16
_7_N:	NOP
_8:	MOV AX,DS:[_I]
	MOV DX,0
	MOV BX,2
	DIV BX
	MOV ES:[4],DX
_9:	MOV DX,1
	MOV AX,ES:[4]
	CMP AX,0
	JE _9_N
	MOV DX,0
_9_N:	MOV ES:[6],DX
_10:	MOV AX,ES:[6]
	CMP AX,0
	JNE _10_N
	JMP FAR PTR _13
_10_N:	NOP
_11:	MOV AX,DS:[_SUM]
	ADD AX,DS:[_I]
	MOV ES:[8],AX
_12:	MOV AX,ES:[8]
	MOV DS:[_SUM],AX
_13:	MOV AX,DS:[_I]
	ADD AX,1
	MOV ES:[10],AX
_14:	MOV AX,ES:[10]
	MOV DS:[_I],AX
_15:	JMP FAR PTR _6
_16:	MOV AX,DS:[_SUM]
	PUSH AX
_17:	CALL _WRITE
	MOV ES:[12],AX
QUIT:	MOV AH,4CH
	INT 21H


_read:	push bp
	mov bp,sp
	mov bx,offset _msg_s
	call _print
	mov bx,offset _buff_s
	mov di,0
_r_lp_1:	mov ah,1
	int 21h
	cmp al,0dh
	je _r_brk_1
	mov ds:[bx+di],al
	inc di
	jmp short _r_lp_1
_r_brk_1:	mov ah,2
	mov dl,0ah
	int 21h
	mov ax,0
	mov si,0
	mov cx,10
_r_lp_2:	mov dl,ds:[bx+si]
	cmp dl,30h
	jb _r_brk_2
	cmp dl,39h
	ja _r_brk_2
	sub dl,30h
	mov ds:[bx+si],dl
	mul cx
	mov dl,ds:[bx+si]
	mov dh,0
	add ax,dx
	inc si
	jmp short _r_lp_2
_r_brk_2:	mov cx,di
	mov si,0
_r_lp_3:	mov byte ptr ds:[bx+si],0
	loop _r_lp_3
	mov sp,bp
	pop bp
	ret

_write:	push bp
	mov bp,sp
	mov bx,offset _msg_p
	call _print
	mov ax,ss:[bp+4]
	mov bx,10
	mov cx,0
_w_lp_1:	mov dx,0
	div bx
	push dx
	inc cx
	cmp ax,0
	jne _w_lp_1
	mov di ,offset _buff_p
_w_lp_2:	pop ax
	add ax,30h
	mov ds:[di],al
	inc di
	loop _w_lp_2
	mov dx,offset _buff_p
	mov ah,09h
	int 21h
	mov cx,di
	sub cx,offset _buff_p
	mov di,offset _buff_p
_w_lp_3:	mov al,24h
	mov ds:[di],al
	inc di
	loop _w_lp_3
	mov ax,di
	sub ax,offset _buff_p
	mov sp,bp
	pop bp
	ret 2
_print:	mov si,0
	mov di,offset _buff_p
_p_lp_1:	mov al,ds:[bx+si]
	cmp al,0
	je _p_brk_1
	mov ds:[di],al
	inc si
	inc di
	jmp short _p_lp_1
_p_brk_1:	mov dx,offset _buff_p
	mov ah,09h
	int 21h
	mov cx,si
	mov di,offset _buff_p
_p_lp_2:	mov al,24h
	mov ds:[di],al
	inc di
	loop _p_lp_2
	ret
code ends

end start

