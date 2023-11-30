from appManager import AppManager

if __name__ == "__main__":
    app_manager = AppManager()
    try:
        app_manager.start()
    except KeyboardInterrupt:
        pass
    finally:
        app_manager.stop()
