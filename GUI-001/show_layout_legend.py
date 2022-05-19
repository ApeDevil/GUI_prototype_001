import pickle
import sys

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.lang import Builder
from screeninfo import get_monitors

print('-------layer legend-----------')
print('arguments: ', sys.argv)
# print('layer: ', sys.argv[1])

for monitor in get_monitors():
    width = monitor.width
    height = monitor.height
    print(monitor)
    print(str(width) + 'x' + str(height))

print(width)
print(height)

Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)


class MainWidget(Widget):

    def on_kv_post(self, *args):
        if len(sys.argv) == 1:
            self.ids.id_layerLabel.text = 'NEW TEST'
            l = 'new_test'
        else:
            self.ids.id_layerLabel.text = sys.argv[1]
            l = sys.argv[1]

        with open('layouts/' + l + '.pickle', 'rb') as f:
            buttonDictLeft = pickle.load(f)
            buttonDictRight = pickle.load(f)

        i=0
        for key in buttonDictLeft.keys():
            if i==25:
                break
            i+=1

            mu1a = '[color=#00ffff]'
            mu1e = '[/color]'
            mu2a = '[color=#ffff00]'
            mu2e = '[/color]'

            b = buttonDictLeft[key]
            t3 = f'self.ids.{key}.text = """{mu1a}{b.Shortcut}{mu1e}\n{mu2a}{b.Description}{mu2e}"""'
            exec(t3)

        J=0
        for key in buttonDictRight.keys():
            if J==25:
                break
            J+=1

            mu1a = '[color=#00ffff]'
            mu1e = '[/color]'
            mu2a = '[color=#ffff00]'
            mu2e = '[/color]'

            b = buttonDictRight[key]
            t3 = f'self.ids.{key}.text = """{mu1a}{b.Shortcut}{mu1e}\n{mu2a}{b.Description}{mu2e}"""'
            exec(t3)






    def on_touch_down(self, touch):
        u = round(touch.x / self.width, 3)
        v = round(touch.y / self.height, 3)
        print(u, v)

        # x = 'buffalo'
        # exec("%s = %d" % (x, 2))
        # print(buffalo)


kv = Builder.load_file('show_layout_legend.kv')


class showLayerLegend(App):
    def build(self):
        return kv


if __name__ == "__main__":
    showLayerLegend().run()
