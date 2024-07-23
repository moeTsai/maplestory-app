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
// 設定圖片搜索範圍，整個螢幕
Const ScreenX1 = 0
Const ScreenY1 = 0
Const ScreenX2 = 1920
Const ScreenY2 = 1080

// 搜索圖片
UserVar overallDelay = 500 "總體延遲"
UserVar numberOfVideos = 1 "錄製影片數量"
UserVar ImagePath = ".\img\" "圖片資料夾位置"

For numberOfVideos
	
	//開始錄製並放大
	call 開始錄製並放大()
	
	Do
    	FindPic ScreenX1, ScreenY1, ScreenX2, ScreenY2, ImagePath + "結束.bmp", 0.99, x, y
    	If x > - 1  And y > - 1  Then 
    		Call 找到結束按鈕()
        	Exit Do
    	End If
    	// 等待3秒後再次搜索
    	Delay 3000
	Loop

Next



Function 開始錄製並放大()
   TracePrint "開始錄製並放大"
   //開始錄製
   MoveTo ScreenX2 - 100, ScreenY2 - 70
   LeftClick 1
   Delay overallDelay
   
   //按回去網頁
   MoveTo ScreenX1 + 960, ScreenY1 + 20
   LeftClick 1
   
   //開始影片並全螢幕
   MoveTo ScreenX1 + 640, ScreenY1 + 360
   LeftClick 1
   Delay overallDelay
   KeyPress "F", 1
End Function

Function 找到結束按鈕()
   TracePrint "找到結束按鈕"
   KeyPress "esc", 1
   
   //停止錄製
   MoveTo ScreenX2 - 100, ScreenY2 - 70
   LeftClick 1
   Delay overallDelay
   
   //下一部影片
   MoveTo ScreenX1 + 1260, ScreenY1 + 410
   LeftClick 1
   Delay overallDelay
   
End Function