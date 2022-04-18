# import serial
# import time
import os
import pickle
import subprocess
import shutil

from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

# import buttons
from buttons import leftDeviceDict, rightDeviceDict
from port_connection import availableDevicesDict  # port_connection.py

# from kivy.uix.button import Button
# from kivy.properties import ListProperty
# from kivy.core.window import Window
# Window.size = (1024, 600)

Config.set('graphics', 'width', '1067')
Config.set('graphics', 'height', '600')


# -------Functions-------Functions-------Functions-------Functions
def call_layout_legend(layer):
    # layer = 'testLayer'
    args = f'python3 show_layout_legend.py {layer}'
    subprocess.Popen(args, shell=True)


# -----GUI-----GUI-----GUI-----GUI-----GUI-----GUI-----GUI-----GUI-----GUI

class MainWindow(Screen):

    def on_kv_post(self, *args):
        print('-------on kv post---------')
        lDL = self.leftDevicesList()
        rDL = self.rightDevicesList()
        print('ldl: ' + str(lDL))
        print('rdl: ' + str(rDL))
        with open('user/last_session.pickle', 'rb') as f:
            lastActiveLayer = pickle.load(f)
            lastActiveLeftDevice = pickle.load(f)
            lastActiveRightDevice = pickle.load(f)
        print('lastLD: ' + lastActiveLeftDevice)
        print('lastRD: ' + lastActiveRightDevice)

        if lastActiveLeftDevice in lDL:
            print('left loaded:' + lastActiveLeftDevice)
            self.addCatWidgets(lastActiveLeftDevice)
            self.ids.id_spinner_LD.text = lastActiveLeftDevice
        elif not lDL:
            print(f'##### no left device')
        else:
            self.addCatWidgets(lDL[0])
            self.ids.id_spinner_LD.text = lDL[0]

        if lastActiveRightDevice in rDL:
            print('right loaded:' + lastActiveRightDevice)
            self.addCatWidgets(lastActiveRightDevice)
            self.ids.id_spinner_RD.text = lastActiveRightDevice
        elif not rDL:
            print(f'##### no right device')
        else:
            self.addCatWidgets(rDL[0])
            self.ids.id_spinner_RD.text = rDL[0]

    def readLayerList(self):
        LL = os.listdir('layouts')
        LayerList = [x.split('.')[0] for x in LL]
        self.ids.id_layer_spinner.values = LayerList
        return LayerList

    def readSubayerList(self):
        SublaerList = ['main', 'second']
        return SublaerList

    def leftDevicesList(self):
        devices = availableDevicesDict.keys()
        lDL = []
        for device in devices:
            DeviceSide = device[0:2]
            if DeviceSide == 'CL':
                lDL.append(device)
        return lDL

    def rightDevicesList(self):
        devices = availableDevicesDict.keys()
        rDL = []
        for device in devices:
            DeviceSide = device[0:2]
            if DeviceSide == 'CR':
                rDL.append(device)
        return rDL

    def saveLastSession(self):
        lastActiveLayer = self.ids.id_layer_spinner.text
        lastActiveLeftDevice = self.ids.id_spinner_LD.text
        lastActiveRightDevice = self.ids.id_spinner_RD.text
        with open('user/last_session.pickle', 'wb') as f:
            pickle.dump(lastActiveLayer, f)
            pickle.dump(lastActiveLeftDevice, f)
            pickle.dump(lastActiveRightDevice, f)

    def loadLastActiveLayer(self):
        with open('user/last_session.pickle', 'rb') as f:
            lastActiveLayer = pickle.load(f)
        return lastActiveLayer

    def addCatWidgets(self, device):
        DeviceSide = device[0:2]
        FM = device[3:6]
        TM = device[7:10]
        # left device
        if DeviceSide == 'CL':
            self.ids.id_LWidgets.clear_widgets()

            if 'B' in FM:
                self.ids.id_LWidgets.add_widget(LeftFingerButtons())
            if 'W' in FM:
                self.ids.id_LWidgets.add_widget(LeftWheel())

            if 'T' in TM:
                self.ids.id_LWidgets.add_widget(LeftThumbTrackball())
            elif 'J' in TM:
                self.ids.id_LWidgets.add_widget(LeftThumbJoystick())
            else:
                self.ids.id_LWidgets.add_widget(LeftThumbButtons())
        # right device
        if DeviceSide == 'CR':
            self.ids.id_RWidgets.clear_widgets()

            if 'B' in FM:
                self.ids.id_RWidgets.add_widget(RightFingerButtons())
            if 'W' in FM:
                self.ids.id_RWidgets.add_widget(RightWheel())

            if 'T' in TM:
                self.ids.id_RWidgets.add_widget(RightThumbTrackball())
            elif 'J' in TM:
                self.ids.id_RWidgets.add_widget(RightThumbJoystick())
            else:
                self.ids.id_RWidgets.add_widget(RightThumbButtons())

    def testPrint(self):
        pass

    def transmitBytes(self):
        print('---------------sending data------------------')
        with open('layouts/' + self.ids.id_layer_spinner.text + '.pickle', 'rb') as f:
            buttonDictLeft = pickle.load(f)
            buttonDictRight = pickle.load(f)

        BytesPacketLeft = bytearray(b'')
        BytesPacketRight = bytearray(b'')
        delimiter = bytearray(b'\xff')
        strEnder = bytearray(b'\xfa')

        # left
        if self.ids.id_spinner_LD.text == 'no left device':
            portL = 'no device'
            pass
        else:
            for b in buttonDictLeft.values():
                BytesPacketLeft.extend(b.KeySet)
                BytesPacketLeft.extend(delimiter)
            BytesPacketLeft.extend(strEnder)
            portL = availableDevicesDict[self.ids.id_spinner_LD.text]
            # portL.open()
            portL.write(BytesPacketLeft)
            # portL.close()

        # right
        if self.ids.id_spinner_RD.text == 'no right device':
            portR = 'no device'
            pass
        else:
            for b in buttonDictRight.values():
                BytesPacketRight.extend(b.KeySet)
                BytesPacketRight.extend(delimiter)
            BytesPacketRight.extend(strEnder)
            portR = availableDevicesDict[self.ids.id_spinner_RD.text]
            # portR.open()
            portR.write(BytesPacketRight)
            # portR.flush()
            # portR.close()

        print(f'left port: {portL}')
        print(f'right port: {portR}')
        print(f'BytesPacketLeft: {BytesPacketLeft}')
        print(f'BytesPacketRight: {BytesPacketRight}')
        print('----Bytes transmitted----')

    def show_layout_legend(self):
        call_layout_legend(self.ids.id_layer_spinner.text)


class LeftFingerButtons(Widget):
    pass


class LeftThumbButtons(Widget):
    pass


class LeftThumbJoystick(Widget):
    pass


class LeftThumbTrackball(Widget):
    pass


class LeftWheel(Widget):
    pass


class RightFingerButtons(Widget):
    pass


class RightThumbButtons(Widget):
    pass


class RightThumbJoystick(Widget):
    pass


class RightThumbTrackball(Widget):
    pass


class RightWheel(Widget):
    pass


################################################################
class LayoutMenu(Screen):

    def saveNewLayout(self, LayerTitle):
        print(f'New Layer created: {LayerTitle}')
        with open('layouts/' + LayerTitle + '.pickle', 'wb') as f:
            pickle.dump(leftDeviceDict, f)
            pickle.dump(rightDeviceDict, f)

    def readLayouts(self):
        LL = os.listdir('layouts')
        LayoutList = [x.split('.')[0] for x in LL]
        self.ids.id_layoutSpinner.values = LayoutList
        return LayoutList

    def copyLayout(self):
        layout = self.ids.id_layoutSpinner.text
        if layout == 'Existing Layouts':
            self.ids.id_messageLabel.text = 'Select Layout !!!'
        else:
            src = f'layouts/{layout}.pickle'
            dst = f'layouts/{layout}_copy.pickle'
            self.ids.id_messageLabel.text = f'Layout -{layout}- was copied.'
            shutil.copyfile(src, dst)

    def renameLayout(self):
        newTitle = self.ids.id_LayoutTitle.text
        layout = self.ids.id_layoutSpinner.text
        if newTitle == '':
            self.ids.id_messageLabel.text = 'Type in new Layout Title !!!'
        elif layout == 'Existing Layouts':
            self.ids.id_messageLabel.text = 'Select Layout !!!'
        else:
            src = f'layouts/{layout}.pickle'
            dst = f'layouts/{newTitle}.pickle'
            os.rename(src, dst)
            self.ids.id_messageLabel.text = f'Layout -{layout}- was renamed to -{newTitle}-.'

    def deleteLayout(self):
        layout = self.ids.id_layoutSpinner.text
        if layout == 'Existing Layouts':
            self.ids.id_messageLabel.text = 'Select Layout !!!'
        else:
            src = f'layouts/{layout}.pickle'
            os.remove(src)
            self.ids.id_messageLabel.text = f'Layout -{layout}- was deleted.'

    def add_sublayer(self):
        # self.ids.id_test.add_widget(Button(text='test'))
        self.ids.id_sublayerLayout.add_widget(SubLayerWidget())


class SubLayerWidget(Widget):
    pass


######################################################################
class ButtonAssignment(Screen):
    currentKeySet = bytearray()
    shortcutText: str = ''

    def saveButtonFunktion(self, Layer, Title, Description):
        print('--save--')
        print(f'------button Layer: {Layer}')
        print(f'------button title: {Title}')
        print(f'------button KeySet: {self.currentKeySet}')
        print(f'---button shortcut: {self.shortcutText}')
        print(f'button description: {Description}')

        with open('layouts/' + Layer + '.pickle', 'rb') as f:
            buttonDictLeft = pickle.load(f)
            buttonDictRight = pickle.load(f)
        # seve left handed layer
        if Title[0] == 'L':
            print('left handed device')
            buttonDictLeft[Title].KeySet = self.currentKeySet
            buttonDictLeft[Title].Shortcut = self.shortcutText
            buttonDictLeft[Title].Description = Description
        # save right handed layer
        else:
            print('right handed device')
            buttonDictRight[Title].KeySet = self.currentKeySet
            buttonDictRight[Title].Shortcut = self.shortcutText
            buttonDictRight[Title].Description = Description

        with open('layouts/' + Layer + '.pickle', 'wb') as f:
            pickle.dump(buttonDictLeft, f)
            pickle.dump(buttonDictRight, f)

    def assignKey(self, buttonText, hexval):
        # shortcut key-title series
        if self.shortcutText == '':
            self.shortcutText = buttonText
        else:
            self.shortcutText = f'{self.shortcutText} + {buttonText}'
        self.ids.id_lable_shortcut.text = f'Shortcut: {self.shortcutText}'
        # shortcut key-hex series
        self.currentKeySet.append(hexval)
        print(self.currentKeySet)

    # hex to lable
    # self.ids.id_label_hex.text = str(hexval)
    # delete current button assignment
    def deleteBA(self):
        self.currentKeySet = bytearray()
        self.shortcutText = ''
        self.ids.id_lable_shortcut.text = 'Shortcut'
        self.ids.id_ti_button_description.text = ''


class JoystickAssignment(Screen):
    def addLeftJoystick(self):
        self.ids.id_JA_FL.clear_widgets()
        self.ids.id_JA_FL.add_widget(LeftJAssignment())

    def addRightJoystick(self):
        self.ids.id_JA_FL.clear_widgets()
        self.ids.id_JA_FL.add_widget(RightJAssignment())


class TrackballAssignment(Screen):
    def addLeftTrackball(self):
        self.ids.id_TA_FL.clear_widgets()
        self.ids.id_TA_FL.add_widget(LeftTAssignment())

    def addRightTrackball(self):
        self.ids.id_TA_FL.clear_widgets()
        self.ids.id_TA_FL.add_widget(RightTAssignment())


class WheelAssignment(Screen):
    def addLeftWheel(self):
        self.ids.id_WA_FL.clear_widgets()
        self.ids.id_WA_FL.add_widget(LeftWAssignment())

    def addRightWheel(self):
        self.ids.id_WA_FL.clear_widgets()
        self.ids.id_WA_FL.add_widget(RightWAssignment())


class LeftJAssignment(Widget):
    pass


class RightJAssignment(Widget):
    pass


class LeftTAssignment(Widget):
    pass


class RightTAssignment(Widget):
    pass


class LeftWAssignment(Widget):
    pass


class RightWAssignment(Widget):
    pass


#########################################################

class WindowManager(ScreenManager):
    pass


class PopUpLayer(Widget):
    pass


def callPopUpLayer():
    show = PopUpLayer()
    popupWindow = Popup(title='test pop', content=show, size_hint=(.5, .5))
    popupWindow.open()


kv = Builder.load_file('main.kv')


class LYNXApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    LYNXApp().run()
