import curses
from takoui import TakoApp
from getinfo import get_device_fingerprint

def main(stdscr):
    app = TakoApp(stdscr, min_rows=16, min_cols=80, bg_color="#000000", fg_color="#FFFFFF", title="takoui demo")
    app.draw_title()

    hostname, device_info = get_device_fingerprint()
    options = ["Show Device Info", "Exit"]
    while True:
        choice = app.menu(2, 2, options)
        if choice == -1 or options[choice] == "Exit":
            break
        elif options[choice] == "Show Device Info":
            lines = []
            def add_line(k, v, indent=0):
                space = ' ' * indent
                lines.append(f"{space}{k}: {v}")
            add_line("Hostname", device_info.get("hostname"))
            add_line("System", device_info.get("system"))
            add_line("Release", device_info.get("release"))
            add_line("Version", device_info.get("version"))
            add_line("Machine", device_info.get("machine"))
            cpu = device_info.get("cpu", {})
            add_line("CPU Model", cpu.get("model"), 2)
            add_line("CPU Cores", cpu.get("cores"), 2)
            add_line("Memory (GB)", device_info.get("memory_gb"))
            add_line("Disk (GB)", device_info.get("disk_gb"))
            ips = device_info.get("ip_addresses", [])
            add_line("IP Addresses", ", ".join(ips) if ips else "N/A")

            text = "\n".join(lines)
            app.preview_text(10, 2, text, 76, 10)
            app.stdscr.getch()

curses.wrapper(main)
