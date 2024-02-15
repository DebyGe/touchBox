import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.config import Config
import subprocess

class CommandShellApp(App):

    def execute_command(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout
        self.output_label.text = output
        return output

    def get_primary_screen(self):
        output = subprocess.check_output(['xrandr']).decode('utf-8')
        for line in output.split('\n'):
            print(" connected primary" + line)
            if 'Screen 0:' in line:
                return line.split()[0]
            
    def add_button(self, text, on_press=None):
        button = Button(text=text, size_hint=(None, None), size=(300, 100))
        if on_press:
            button.bind(on_press=on_press)
        self.layout.add_widget(button)

    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.output_label = Label(text='', size_hint=(1, None), height=Window.height * 0.5)
        self.layout.add_widget(self.output_label)
 
        self.add_button('Esegui "Wall-of-Flippers"', lambda x: self.execute_command('bash /home/debora/MyDev/Wall-of-Flippers/wof.sh'))
        self.add_button('Esegui "ls -l"', lambda x: self.execute_command('ls -l'))
        self.add_button('Esegui "pwd"', lambda x: self.execute_command('pwd'))

        self.add_button('Chiudi Applicativo', lambda x: self.stop())

        Window.fullscreen = 'auto'  # Imposta a 'True' per fullscreen automatico o 'auto' per rimanere in finestra

        primary_screen = self.get_primary_screen()
        if primary_screen:
            Config.set('graphics', 'fullscreen', 'auto')
            Config.set('graphics', 'borderless', '1')
            Config.set('graphics', 'window_state', 'maximized')
            Config.set('graphics', 'display', primary_screen)

        return self.layout

if __name__ == '__main__':
    CommandShellApp().run()
