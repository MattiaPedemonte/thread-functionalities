import threading
import time

shared_variable = None

lock = threading.Lock()

event_A2B = threading.Event()
event_B2A = threading.Event()

def function_A():
    global shared_variable
    for i in range(3):
        message = f"Message {i} from function_A"
        
        with lock:
            shared_variable = message
            print("function A in writing inside shared_variable")

        event_A2B.set()

        event_B2A.wait()

        with lock:
            print("function_A is reading from shared_memory")
            print(f"{shared_variable=}")

        event_B2A.clear()

def function_B():
    global shared_variable
    for i in range(3):
        message = f"Message {i} from function_B"
        event_A2B.wait()

        with lock:
            print("function_B is reading from shared_memory")
            print(f"{shared_variable= }")

            shared_variable = message
            print("function B in writing inside shared_variable")

        event_B2A.set()

        event_A2B.clear()

if __name__ == "__main__":
    tA = threading.Thread(target=function_A, name="Thread_A")
    tB = threading.Thread(target=function_B, name="Thread_B")

    tA.start()
    tB.start()

    tA.join()
    tB.join()

    print("all the threads have terminated, main can procede")
    for i in range(3):
        print(f"main thread is running {i} time")
        