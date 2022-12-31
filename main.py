from app import App

if __name__ == '__main__':
    app = App((1920, 1080))
    app.cur_scene = app.gs
    app.run()
