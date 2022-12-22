from app import App

if __name__ == '__main__':
    app = App((800, 600))
    app.cur_scene = app.gs
    app.run()
