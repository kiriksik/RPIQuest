from gui import App

# ====== ЗАПУСК ПРИЛОЖЕНИЯ ======
if __name__ == "__main__":


    app = App()

    app.server.connect()
    app.run()
