# feh-browse

Simple background manager using 'feh'.

To set a wallpaper: "feh --bg-max image.png"

This sets a file ~/.fehbg. To restore the wallpaper from .xinitrc: "eval $(cat ~/.fehbg) &"

To restore the file in .config/i3/config: "exec –no-startup-id ~/.fehbg"

TO DO: implement all 'bg' feh options as GUI. Insert into i3 config or .profile as needed. If already present, comment/skip.

