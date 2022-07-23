import os
import re
import json


def parse_uptime_cmd_output(uptime_output):
    uptime_output = uptime_output.strip()
    m = re.match(r".*averages?\:[ \t]*([0-9\.]+)[\, \t]*([0-9\.]+)[\, \t]*([0-9\.]+).*", uptime_output)
    groups = m.groups()
    return {
        "1min": float(groups[0]),
        "5min": float(groups[1]),
        "15min": float(groups[2]),
    }


def parse_free_cmd_output(free_output):
    lines = free_output.split("\n")
    output = {
        "ram": {"total": None, "used": None, "free": None},
        "swap": {"total": None, "used": None, "free": None},
    }
    for line in lines:
        if line.startswith("Mem:"):
            m = re.match(r"Mem:[ \t]*([0-9]+)[ \t]*([0-9]+)[ \t]*([0-9]+)", line)
            groups = m.groups()
            output["ram"] = {
                "total": int(groups[0]),
                "used": int(groups[1]),
                "free": int(groups[2]),
            }
        if line.startswith("Swap:"):
            m = re.match(r"Swap:[ \t]*([0-9]+)[ \t]*([0-9]+)[ \t]*([0-9]+)", line)
            groups = m.groups()
            output["swap"] = {
                "total": int(groups[0]),
                "used": int(groups[1]),
                "free": int(groups[2]),
            }
                    
    return output


def parse_df_cmd_output(df_output):
    df_output = df_output.strip()
    lines = df_output.split("\n")
    output = {}
    for line in lines:
        if line.startswith("Filesystem"):
            continue
        m = re.match((
            r"([0-9\/a-zA-Z _-]+?)[ \t]+"
            r"([0-9]+)[ \t]+"
            r"([0-9]+)[ \t]+"
            r"([0-9]+)[ \t]+"
            r".*"
        ), line)
        if m is None:
            import pdb; pdb.set_trace()
        groups = m.groups()
        output[groups[0]] = {
            "used": int(groups[2]),
            "available": int(groups[3]),
        }

    return output


def main(run_free_cmd, run_uptime_cmd, run_df_cmd):
    output = {
        "memory": parse_free_cmd_output(run_free_cmd()),
        "cpu": parse_uptime_cmd_output(run_uptime_cmd()),
        "disk": parse_df_cmd_output(run_df_cmd()),
    }
    return output

def run_free_command():
    stream = os.popen("free")
    output = stream.read()
    return output


def run_uptime_command():
    stream = os.popen("uptime")
    output = stream.read()
    return output


def run_df_command():
    stream = os.popen("df")
    output = stream.read()
    return output


if __name__ == '__main__':
    output = main(
        run_free_cmd=run_free_command,
        run_uptime_cmd=run_uptime_command,
        run_df_cmd=run_df_command
    )
    print(json.dumps(output, indent=2))

