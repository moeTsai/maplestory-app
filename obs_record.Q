[General]
SyntaxVersion=2
BeginHotkey=121
BeginHotkeyMod=0
PauseHotkey=0
PauseHotkeyMod=0
StopHotkey=123
StopHotkeyMod=0
RunOnce=1
EnableWindow=
MacroID=75849227-89fd-4473-8003-469ca74b9028
Description=obs_record
Enable=1
AutoRun=0
[Repeat]
Type=0
Number=1
[SetupUI]
Type=2
QUI=
[Relative]
SetupOCXFile=
[Comment]

[Script]
// �]�w�Ϥ��j���d��A��ӿù�
Const ScreenX1 = 0
Const ScreenY1 = 0
Const ScreenX2 = 1920
Const ScreenY2 = 1080

// �j���Ϥ�
UserVar overallDelay = 500 "�`�驵��"
UserVar numberOfVideos = 1 "���s�v���ƶq"
UserVar ImagePath = ".\img\" "�Ϥ���Ƨ���m"

For numberOfVideos
	
	//�}�l���s�é�j
	call �}�l���s�é�j()
	
	Do
    	FindPic ScreenX1, ScreenY1, ScreenX2, ScreenY2, ImagePath + "����.bmp", 0.99, x, y
    	If x > - 1  And y > - 1  Then 
    		Call ��쵲�����s()
        	Exit Do
    	End If
    	// ����3����A���j��
    	Delay 3000
	Loop

Next



Function �}�l���s�é�j()
   TracePrint "�}�l���s�é�j"
   //�}�l���s
   MoveTo ScreenX2 - 100, ScreenY2 - 70
   LeftClick 1
   Delay overallDelay
   
   //���^�h����
   MoveTo ScreenX1 + 960, ScreenY1 + 20
   LeftClick 1
   
   //�}�l�v���å��ù�
   MoveTo ScreenX1 + 640, ScreenY1 + 360
   LeftClick 1
   Delay overallDelay
   KeyPress "F", 1
End Function

Function ��쵲�����s()
   TracePrint "��쵲�����s"
   KeyPress "esc", 1
   
   //������s
   MoveTo ScreenX2 - 100, ScreenY2 - 70
   LeftClick 1
   Delay overallDelay
   
   //�U�@���v��
   MoveTo ScreenX1 + 1260, ScreenY1 + 410
   LeftClick 1
   Delay overallDelay
   
End Function