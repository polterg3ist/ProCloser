from subprocess import Popen
from os import path
import psutil


class ProcessManager:
    def __init__(self, w):
        open_method = "r" if path.exists("blacklist.txt") else "w"
        with open("blacklist.txt", open_method) as file:
            if open_method == "r":
                self.black_list = file.readlines()
        self.w = w
        self.running_proc = None

    def running_proc_upd(self):
        self.running_proc = [proc.Name for proc in self.w.Win32_Process()]

    @staticmethod
    def sp_kill(proc_name):
        # Attempt to kill using subprocess module
        Popen(f'taskkill /im {proc_name} /f /t')

    @staticmethod
    def kill_proc_and_children(parent_pid):
        # Attempt to kill using psutil module. This module should also kill the child process of the parent process
        parent = psutil.Process(parent_pid)
        for child in parent.children(recursive=True):  # or parent.children() for recursive=False
            child.kill()
        parent.kill()

    @staticmethod
    def make_log(text):
        open_method = "a" if path.exists('log.txt') else "w"
        with open('log.txt', open_method) as file:
            file.write(f"{text}\n")
