import tkinter

from app import App
from settingframe import SettingFrame


def main():
    root = tkinter.Tk()
    sf = SettingFrame(root)
    sf.mainloop()
    root.destroy()

    root = tkinter.Tk()
    app = App(root, sf.board_size, sf.wall, sf.players)
    app.mainloop()

if __name__ == '__main__':
    main()
