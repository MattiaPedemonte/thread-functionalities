import multiprocessing
import time

def increment_variable(shared_var):
    for _ in range(10):  # reduced number for testing
        print(f"[Increment] Timestamp: {time.time()}")
        with shared_var.get_lock():  # mutex protection, only one function can modify the shared variable at a time
            shared_var.value += 1
            print(f"[Increment] Shared variable = {shared_var.value}")
            time.sleep(0.01)  

def decrement_variable(shared_var):
    for _ in range(10):
        print(f"[Decrement] Timestamp: {time.time()}")
        with shared_var.get_lock():
            shared_var.value -= 1
            print(f"[Decrement] Shared variable = {shared_var.value}")
            time.sleep(0.01)

def main():
    print("Initializing shared variable...")

    shared_var = multiprocessing.Value('i', 0)  # 'i' = integer

    process_inc = multiprocessing.Process(target=increment_variable, args=(shared_var,))
    process_dec = multiprocessing.Process(target=decrement_variable, args=(shared_var,))

    process_inc.start()
    process_dec.start()

    process_inc.join()
    process_dec.join()

    print(f"\n[Main] Final value of shared variable: {shared_var.value}")

if __name__ == "__main__":
    main()
