# Mouse Control

Install the service:

    sudo cp mousecontrol.service /etc/systemd/system/

Add the user to the `input` group so they can access `/dev/input/event*`:

    sudo usermod -a -G input samuel

Restart so the group takes effect, check it's working

    cat /dev/input/event0

Shouldn't show a permissions error.

Copy `mousecontrol.py` to the `ExecStart` path in `mousecontrol.service`.

Log the service output:

    journalctl -u mousecontrol.service -f

Start the service:

    sudo systemctl start mousecontrol.service

With that `mousecontrol.py` should be running.

Run the service at startup:

    sudo systemctl status mousecontrol.service