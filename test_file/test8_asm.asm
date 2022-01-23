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
	_N dw 0
	_M dw 0
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
	MOV DS:[_A],AX
_2:	CALL _READ
	MOV ES:[0],AX
_3:	MOV AX,ES:[0]
	MOV DS:[_N],AX
_4:	CALL _READ
	MOV ES:[2],AX
_5:	MOV AX,ES:[2]
	MOV DS:[_M],AX
_6:	MOV AX,DS:[_M]
	PUSH AX
_7:	MOV AX,DS:[_N]
	PUSH AX
_8:	CALL _MAX
	MOV ES:[4],AX
_9:	MOV AX,ES:[4]
	PUSH AX
_10:	MOV AX,100
	PUSH AX
_11:	CALL _SUM
	MOV ES:[6],AX
_12:	MOV AX,ES:[6]
	MOV DS:[_A],AX
_13:	MOV AX,DS:[_A]
	PUSH AX
_14:	CALL _WRITE
	MOV ES:[8],AX
QUIT:	MOV AH,4CH
	INT 21H


_SUM:	PUSH BP
	MOV BP,SP
	SUB SP,2
_17:	MOV AX,SS:[BP+6]
	ADD AX,SS:[BP+4]
	MOV ES:[10],AX
_18:	MOV AX,ES:[10]
	MOV SS:[BP-2],AX
_19:	MOV AX,SS:[BP-2]
	MOV SP,BP
	POP BP
	RET 4
_20:	MOV SP,BP
	POP BP
	RET 4

_MAX:	PUSH BP
	MOV BP,SP
	SUB SP,2
_22:	MOV DX,1
	MOV AX,SS:[BP+6]
	CMP AX,SS:[BP+4]
	JNB _22_N
	MOV DX,0
_22_N:	MOV ES:[12],DX
_23:	MOV AX,ES:[12]
	CMP AX,0
	JNE _23_N
	JMP FAR PTR _26
_23_N:	NOP
_24:	MOV AX,SS:[BP+6]
	MOV SS:[BP-2],AX
_25:	JMP FAR PTR _27
_26:	MOV AX,SS:[BP+4]
	MOV SS:[BP-2],AX
_27:	MOV AX,SS:[BP-2]
	MOV SP,BP
	POP BP
	RET 4
_28:	MOV SP,BP
	POP BP
	RET 4

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

