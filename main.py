import window
import queue

debug = True

def main():
    update_queue = queue.Queue()
    window.CreateWindow("Hangman", debug, update_queue)

if __name__ == "__main__":
    main()