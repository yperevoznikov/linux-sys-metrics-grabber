from dump_system_metrics import parse_free_cmd_output, parse_uptime_cmd_output, parse_df_cmd_output

def _run_fake_free_cmd():
    return """              total        used        free      shared  buff/cache   available
Mem:        4026648      744056      278024        4184     3004568     2991392
Swap:       4026364      380604     3645760"""


def _run_fake_uptime_cmd_v1():
    return "12:25  up 7 days, 32 mins, 2 users, load averages: 2.74 2.24 2.08"


def _run_fake_uptime_cmd_v2():
    return " 03:55:37 up 458 days, 10:46,  5 users,  load average: 0.10, 0.04, 0.01"


def _run_fake_df_cmd_v1():
    return """Filesystem    512-blocks       Used Available Capacity iused      ifree %iused  Mounted on
/dev/disk1s1  1953595632   21956096 692848056     4%  488382 9767489778    0%   /
devfs                390        390         0   100%     676          0  100%   /dev
/dev/disk1s2  1953595632 1224605312 692848056    64% 5581465 9762396695    0%   /System/Volumes/Data
/dev/disk1s5  1953595632   12582992 692848056     2%       6 9767978154    0%   /private/var/vm
map auto_home          0          0         0   100%       0          0  100%   /System/Volumes/Data/home"""


def _run_fake_df_cmd_v2():
    return """Filesystem                         1K-blocks     Used Available Use% Mounted on
tmpfs                                 402668     1576    401092   1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv   40506624 28057280  10362024  74% /
tmpfs                                2013324        0   2013324   0% /dev/shm
tmpfs                                   5120        0      5120   0% /run/lock
tmpfs                                   4096        0      4096   0% /sys/fs/cgroup
/dev/sda2                             999320   325072    605436  35% /boot
/dev/mapper/ubuntu--vg-primary--lv  40502528    49176  38366236   1% /mnt/primary
tmpfs                                 402664        4    402660   1% /run/user/1001
overlay                             40506624 28057280  10362024  74% /var/lib/docker/overlay2/1763922f77a126b57bad74a74f236a48e8c58d2c4ebefe47bcf93b7ce9f941da/merged
overlay                             40506624 28057280  10362024  74% /var/lib/docker/overlay2/f53e5a414e7a839da9f3099653181d92a616c05e4f6725c0b53bd66dafaad25d/merged
overlay                             40506624 28057280  10362024  74% /var/lib/docker/overlay2/05bc1f4e768545d217c40e2e4311ed7ccd4052325b00dfe3124cea079e639d43/merged
shm                                    65536        0     65536   0% /var/lib/docker/containers/9de18a4911eded6cadbbf965ad27827a3dded30d468bf82b6feb47b77becdfdc/mounts/shm
shm                                    65536        0     65536   0% /var/lib/docker/containers/f0c6c11196b98570e30853d4b2b2ab9eb8b39255e16fb13a9c020b3d054d6b92/mounts/shm
overlay                             40506624 28057280  10362024  74% /var/lib/docker/overlay2/7fd950a09ab47029e7b9330bb79263920a20263139b52284b6f88494cd6688aa/merged
shm                                    65536        0     65536   0% /var/lib/docker/containers/e1f4ef5faafb012204fb20799c8c7ad50c4019229cd9fe0b50b8575acc04db03/mounts/shm
overlay                             40506624 28057280  10362024  74% /var/lib/docker/overlay2/1ae75e12940feca62794eb41c3f252cef02f4ccd16164756a748355140baf3ce/merged
shm                                    65536        0     65536   0% /var/lib/docker/containers/f07795243862c1e3be653f9883e07ce516320f6a2318fad60d304c08f26f9fd5/mounts/shm"""


def test_parse_free_cmd_output():
    output = parse_free_cmd_output(_run_fake_free_cmd())

    assert "ram" in output
    assert output["ram"]["total"] == 4026648
    assert output["ram"]["used"] == 744056
    assert output["ram"]["free"] == 278024
    assert "swap" in output
    assert output["swap"]["total"] == 4026364
    assert output["swap"]["used"] == 380604
    assert output["swap"]["free"] == 3645760


def test_parse_free_cmd_output_failure():
    output = parse_free_cmd_output("")

    assert "ram" in output
    assert output["ram"]["total"] == None
    assert output["ram"]["used"] == None
    assert output["ram"]["free"] == None
    assert "swap" in output
    assert output["swap"]["total"] == None
    assert output["swap"]["used"] == None
    assert output["swap"]["free"] == None


def test_parse_uptime_cmd_output_v1():
    output = parse_uptime_cmd_output(_run_fake_uptime_cmd_v1())

    assert output["1min"] == 2.74
    assert output["5min"] == 2.24
    assert output["15min"] == 2.08


def test_parse_uptime_cmd_output_v2():
    output = parse_uptime_cmd_output(_run_fake_uptime_cmd_v2())

    assert output["1min"] == 0.10
    assert output["5min"] == 0.04
    assert output["15min"] == 0.01


def test_parse_df_cmd_output_v1():
    output = parse_df_cmd_output(_run_fake_df_cmd_v1())

    # Test first FS row
    assert "/dev/disk1s1" in output
    assert output["/dev/disk1s1"]["used"] == 21956096
    assert output["/dev/disk1s1"]["available"] == 692848056

    # Test other FSs
    assert "devfs" in output
    assert "/dev/disk1s2" in output
    assert "/dev/disk1s5" in output
    assert "map auto_home" in output


def test_parse_df_cmd_output_v2():
    output = parse_df_cmd_output(_run_fake_df_cmd_v2())

    # Test first FS row
    assert "tmpfs" in output
    # TODO: improve this test: add more asserts

