from __future__ import annotations

import json
import os
import sys
import time
import urllib.request


BASE = "http://localhost:8222"


def submit_task(task_json_path: str) -> str:
    with open(task_json_path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(
        f"{BASE}/queue/management/tasks/submit",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    resp = json.loads(urllib.request.urlopen(req).read().decode())
    return resp["task_id"]


def get_task_info(task_id: str) -> dict:
    return json.loads(
        urllib.request.urlopen(f"{BASE}/queue/management/tasks/info/{task_id}").read().decode()
    )


def get_task_logs(task_id: str, latest_only: bool = True) -> str:
    flag = "true" if latest_only else "false"
    try:
        return urllib.request.urlopen(
            f"{BASE}/queue/management/logs/{task_id}?latest_only={flag}"
        ).read().decode()
    except Exception as e:
        return f"NO_LOGS: {e}"


def list_outputs(root: str) -> tuple[list[str], list[str]]:
    if not os.path.isdir(root):
        return [], []
    files = os.listdir(root)
    exr = [n for n in files if n.lower().endswith(".exr")]
    png = [n for n in files if n.lower().endswith(".png")]
    return exr, png


def main() -> int:
    task_json = sys.argv[1] if len(sys.argv) > 1 else "task_hello_world.json"
    out_dir = r"D:\\NVIDIA-Omniverse\\kit-app-template\\render_output"

    task_id = submit_task(task_json)
    print(f"TASK_ID={task_id}")

    # brief poll for status
    for _ in range(20):
        info = get_task_info(task_id)
        print(f"STATUS={info.get('status')}")
        if info.get("status") in {"finished", "failed"}:
            break
        time.sleep(0.6)

    # logs
    logs = get_task_logs(task_id, latest_only=True)
    print("--- LOGS (head) ---")
    print(logs[:1000])

    # outputs
    exr, png = list_outputs(out_dir)
    print("--- OUTPUT EXR ---")
    for n in exr:
        print(n)
    print("--- OUTPUT PNG ---")
    for n in png:
        print(n)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
