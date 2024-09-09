from gui import ChatApp

from datetime import datetime
start_time = datetime.now()


def main():
    try:
        app = ChatApp()  # Initialize the ChatApp
        app.run()        # Run the ChatApp
    except Exception as e:
        print(f"Error starting the application: {e}")

if __name__ == "__main__":
    main()






#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
