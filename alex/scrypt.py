import os
import signal
import time

def pause_game(pid):
        os.kill(pid, signal.SIGSTOP)
        print(f"Process {pid} paused.")


def resume_game(pid):
        os.kill(pid, signal.SIGCONT)
        print(f"Process {pid} resumed.")


if __name__ == "__main__":
    pid = int(input("Enter the PID of the game process: "))
    
    # Mettre en pause le jeu pendant 5 secondes
    pause_game(pid)
    time.sleep(5)
    
    # Relancer le jeu après la pause
    resume_game(pid)
