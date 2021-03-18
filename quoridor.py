import tkinter

from app import App


def main():
    root = tkinter.Tk()
    app = App(root)
    app.mainloop()


if __name__ == '__main__':
    main()
