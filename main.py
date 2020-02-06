import serial
import time
import wx
import threading
import winsound

frequency = 1000  # Set Frequency To 2500 Hertz
frequency2 = 2000  # Set Frequency To 2500 Hertz
frequency3 = 3000  # Set Frequency To 2500 Hertz

duration = 1000  # Set Duration To 1000 ms == 1 second

connected = False
port = 'COM4'
baud = 9600
ups1 = ''
my_string = str(ups1)
data = ''
alarm = ''
my_string2 = str(alarm)

filename = 'ac-ok.wav'
filename2 = 'dc-ok.wav'
filename3 = 'f-alarm.wav'
filename4 = 't-alarm.wav'

class ExamplePanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, pos=(500, 500), size=(500, 500), name="Power Maintenance v.0.1:")
        #self.thread = threading.Thread(target=self.read_from_port, args=(self.serial_port, self.callback))
        #self.thread.start()
        self.serial_port = serial.Serial(port, baud, timeout=0.1)
        self.quote = wx.StaticText(self, label="Power Maintenance v.0.1:", pos=(10, 10))
        # Весь вывод
        self.logger = wx.TextCtrl(self, pos=(390, 20), size=(390, 20), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Кнопки для управления блоком
        self.button = wx.Button(self, label="Включить", pos=(10, 140))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button = wx.Button(self, label="Выключить", pos=(120, 140))
        self.Bind(wx.EVT_BUTTON, self.OnClick2, self.button)
        self.button = wx.Button(self, label="Считать", pos=(240, 140))
        self.Bind(wx.EVT_BUTTON, self.OnClick3, self.button)

        # Ввод комманд
        self.lblname = wx.StaticText(self, label="Введите команду:", pos=(20, 60))
        self.editname = wx.TextCtrl(self, value="", pos=(150, 60), size=(140, -1))
        self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)

        # Управление выходным напряжением
        self.sampleList = ['43‬', '48', '53']
        self.lblhear = wx.StaticText(self, label="Выходное напряжение", pos=(20, 90))
        self.edithear = wx.ComboBox(self, pos=(150, 90), size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.edithear)

        # Флажок
        self.insure = wx.CheckBox(self, label="Вы включили нагрузку к блоку?", pos=(20, 120))
        self.Bind(wx.EVT_CHECKBOX, self.onChecked)
        self.Centre()
        self.Show(True)

        # Словарь команд
        self.label = wx.StaticText(self, label="Словарь команд", pos=(20, 170))
        self.label = wx.StaticText(self, label="H-Включить", pos=(20, 190))
        self.label = wx.StaticText(self, label="L-Выключить", pos=(20, 210))
        self.label = wx.StaticText(self, label="R-Разрешить подачу выходного напряжения", pos=(20, 230))
        self.label = wx.StaticText(self, label="W-Запретить подачу выходного напряжения", pos=(20, 250))
        self.label = wx.StaticText(self, label="C-Считать аварию", pos=(20, 270))
        self.label = wx.StaticText(self, label="T-Считать всю информацию", pos=(20, 290))
    # def EvtRadioBox(self, event):
    #    self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())

    def OnClick(self, event):
        self.logger.AppendText(" Click on object with Id %d\n" % event.GetId())
        print("Включить")
        self.serial_port.write(b'H')

    def OnClick2(self, event):
        self.logger.AppendText(" Click on object with Id %d\n" % event.GetId())
        print("Выключить")
        self.serial_port.write(b'L')

    def OnClick3(self, event):
        self.logger.AppendText(" Click on object with Id %d\n" % event.GetId())
        print("Считать параметры")
        ups1 = self.serial_port.readline().decode()
        print(ups1)
        time.sleep(0.2)
        if ups1 == "1":
            winsound.Beep(frequency, duration)
            winsound.PlaySound(filename, winsound.SND_FILENAME)
            print("ALARM_A1")
            alarm = 1
            my_string2 = str(alarm)
            print('alarm', alarm)
            handle = open("output.txt", "w")
            handle.write(ups1)
            handle.write(my_string2)
            handle.write("my_string2_1")
            self.serial_port.write(b'T1')
            handle.write(ups1)
            handle.close()
        elif ups1 == "2":
            winsound.Beep(frequency2, duration)
            winsound.PlaySound(filename2, winsound.SND_FILENAME)
            print("ALARM_A2")
            alarm = 2
            my_string2 = str(alarm)
            print('alarm', alarm)
            handle = open("output.txt", "w")
            handle.write(ups1)
            handle.write(my_string2)
            handle.write("my_string2_2")
            self.serial_port.write(b'T2')
            handle.write(ups1)
            handle.close()
        elif ups1 == "3":
            winsound.Beep(frequency3, duration)
            winsound.PlaySound(filename3, winsound.SND_FILENAME)
            print("ALARM_A3")
            alarm = 3
            my_string2 = str(alarm)
            handle = open("output.txt", "w")
            handle.write(ups1)
            handle.write(my_string2)
            handle.write("my_string2_3")
            self.serial_port.write(b'T3')
            handle.write(ups1)
            handle.close()

    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
        print("command work")
        print('EvtText: %s\n' % event.GetString())
        self.serial_port.write(event.GetString().encode('utf-8'))

    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()

    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
        print("RUN")

    def onChecked(self, e):
        cb = e.GetEventObject()
        print(cb.GetValue())
        cb.GetLabel(), 'is clicked', cb.GetValue()
        if cb.GetValue() == True:
            print("RUN")
            self.serial_port.write(b'R')
        elif cb.GetValue() == False:
            print("POWER")
            self.serial_port.write(b'W')


app = wx.App(False)
frame = wx.Frame(None)
panel = ExamplePanel(frame)
#panel.thread.start()
frame.Show()
print("POWER")
app.MainLoop()