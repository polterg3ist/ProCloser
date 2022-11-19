from process_manager import ProcessManager
import time
import settings
import wmi


def main():

    w = wmi.WMI()
    pm = ProcessManager(w)

    pm.make_log(f"{'-'*80}\n{time.asctime()}\n")

    while True:
        for proc in w.Win32_Process():
            if proc.Name in pm.black_list:
                try:
                    for pr in (p for p in w.Win32_Process() if p.Name == proc.Name):
                        pr.Terminate()                                      # first attempt to kill
                        pm.running_proc_upd()
                        if not proc.Name in pm.running_proc:
                            break
                    if proc.Name in pm.running_proc:
                        pm.sp_kill(proc.Name)                               # second attempt to kill
                        pm.running_proc_upd()
                        if proc.Name in pm.running_proc:
                            pm.kill_proc_and_children(proc.ProcessId)       # third attempt to kill
                            pm.running_proc_upd()
                except Exception as ex:
                    pm.make_log(f"Exception {ex} occurred with process {proc.Name}")
                else:
                    if proc.Name in pm.running_proc:
                        pm.make_log(f"Can't kill {proc.Name} after all attempts")
                    else:
                        pm.make_log(f"{proc.Name} was successfully killed")

        if settings.ALL_TIME_ACTIVE:
            time.sleep(settings.AFTER_TIME_RUN)
        else:
            pm.make_log(f"\nProgram finished. Time: {time.asctime()}")
            break


if __name__ == "__main__":
    main()
