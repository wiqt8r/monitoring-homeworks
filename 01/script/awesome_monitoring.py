#!/usr/bin/env python3
import json
import os
import time
from datetime import datetime

LOG_DIR = "/var/log"
LOG_SUFFIX = "awesome-monitoring.log"

# Для вычисления cpu_usage_percent нужна дельта между запусками
STATE_FILE = "/var/tmp/awesome-monitoring.state.json"


def read_first_line(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.readline().strip()


def parse_load1() -> float:
    # /proc/loadavg: "1.23 0.97 0.88 2/123 4567"
    parts = read_first_line("/proc/loadavg").split()
    return float(parts[0])


def parse_uptime_seconds() -> float:
    # /proc/uptime: "<uptime_seconds> <idle_seconds>"
    parts = read_first_line("/proc/uptime").split()
    return float(parts[0])


def parse_meminfo_bytes() -> dict:
    # /proc/meminfo values in kB
    meminfo = {}
    with open("/proc/meminfo", "r", encoding="utf-8") as f:
        for line in f:
            key, rest = line.split(":", 1)
            value_parts = rest.strip().split()
            if not value_parts:
                continue
            value_kb = int(value_parts[0])
            meminfo[key] = value_kb * 1024

    mem_total = meminfo.get("MemTotal", 0)
    mem_available = meminfo.get("MemAvailable", 0)
    mem_used = max(mem_total - mem_available, 0)

    return {
        "mem_total_bytes": mem_total,
        "mem_available_bytes": mem_available,
        "mem_used_bytes": mem_used,
    }


def parse_netdev_bytes() -> dict:
    # /proc/net/dev: rx bytes is field 1 after iface:, tx bytes is field 9
    rx_total = 0
    tx_total = 0
    with open("/proc/net/dev", "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines[2:]:  # skip headers
        if ":" not in line:
            continue
        iface, data = line.split(":", 1)
        iface = iface.strip()
        # skip loopback
        if iface == "lo":
            continue
        fields = data.strip().split()
        if len(fields) < 16:
            continue
        rx_bytes = int(fields[0])
        tx_bytes = int(fields[8])
        rx_total += rx_bytes
        tx_total += tx_bytes

    return {"net_rx_bytes": rx_total, "net_tx_bytes": tx_total}


def read_cpu_counters() -> dict:
    # /proc/stat first line: cpu  user nice system idle iowait irq softirq steal guest guest_nice
    line = read_first_line("/proc/stat")
    parts = line.split()
    if len(parts) < 5 or parts[0] != "cpu":
        return {"total": 0, "idle": 0}

    # convert all to int jiffies
    values = [int(x) for x in parts[1:]]
    total = sum(values)
    idle = values[3] + (values[4] if len(values) > 4 else 0)  # idle + iowait
    return {"total": total, "idle": idle}


def calc_cpu_usage_percent(prev: dict, cur: dict) -> float:
    prev_total = prev.get("total", 0)
    prev_idle = prev.get("idle", 0)
    cur_total = cur.get("total", 0)
    cur_idle = cur.get("idle", 0)

    total_delta = cur_total - prev_total
    idle_delta = cur_idle - prev_idle
    if total_delta <= 0:
        return 0.0

    usage = (total_delta - idle_delta) / total_delta * 100.0
    # clamp just in case
    return max(0.0, min(100.0, usage))


def load_prev_state() -> dict:
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state: dict) -> None:
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f)
    os.replace(tmp, STATE_FILE)


def get_log_path(now: datetime) -> str:
    filename = now.strftime("%y-%m-%d") + "-" + LOG_SUFFIX
    return os.path.join(LOG_DIR, filename)


def main():
    now = datetime.now()
    ts = int(time.time())

    load1 = parse_load1()
    uptime_seconds = parse_uptime_seconds()
    mem = parse_meminfo_bytes()
    net = parse_netdev_bytes()

    cur_cpu = read_cpu_counters()
    prev_state = load_prev_state()
    prev_cpu = prev_state.get("cpu", {"total": 0, "idle": 0})
    cpu_usage_percent = calc_cpu_usage_percent(prev_cpu, cur_cpu)

    record = {
        "timestamp": ts,
        "load1": load1,
        "cpu_usage_percent": round(cpu_usage_percent, 2),
        "uptime_seconds": uptime_seconds,
        **mem,
        **net,
    }

    log_path = get_log_path(now)

    # write json line
    line = json.dumps(record, ensure_ascii=False)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

    # save state for next run
    save_state({"cpu": cur_cpu})


if __name__ == "__main__":
    main()
