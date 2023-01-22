# Copyright (c) 2011 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, qtile, hook
from bar import my_bar, get_screens_connected
from second_bar import my_second_bar
from third_bar import my_third_bar
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from layouts import custom_layouts
from libqtile.log_utils import logger
import subprocess

mod = "mod4"
terminal = "alacritty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "Return", lazy.layout.shuffle_left(), desc="Make window master"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # For Monad Tall
    Key([mod, "control"], "h", lazy.layout.shrink_main(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_main(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.shrink(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.reset(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn('firefox'), desc="Launch brave browser"),
    Key([mod, "shift"], "Return", lazy.spawn('pcmanfm'), desc="Launch pcmanfm"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn('rofi -show run -icon-theme "Papirus" -show-icons -run-shell-command \'{terminal} -e bash -ic \"{cmd} && read\"\''), desc="Spawn a command using a prompt widget"),
    # DropDown Terminal
    Key([mod, "control"], "t", lazy.group["scratchpad"].dropdown_toggle("term")),
]

def go_to_group(name: str):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.groups_map[name].cmd_toscreen()
            return

        if name in '1234':
            qtile.focus_screen(0)
            qtile.groups_map[name].cmd_toscreen()
        elif name in '5678':
            qtile.focus_screen(1)
            qtile.groups_map[name].cmd_toscreen()
        else:
            qtile.focus_screen(2)
            qtile.groups_map[name].cmd_toscreen()

    return _inner

def go_to_group_and_move_window(name: str):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.current_window.cmd_togroup(name, switch_group=True)
            return

        if name in '1234':
            qtile.current_window.cmd_togroup(name, switch_group=False)
            qtile.focus_screen(0)
            qtile.groups_map[name].cmd_toscreen()
        elif name in '5678':
            qtile.current_window.cmd_togroup(name, switch_group=False)
            qtile.focus_screen(1)
            qtile.groups_map[name].cmd_toscreen()
        else:
            qtile.current_window.cmd_togroup(name, switch_group=False)
            qtile.focus_screen(2)
            qtile.groups_map[name].cmd_toscreen()

    return _inner

# Append a drop-down termainal
groups = [ Group(f"{i+1}", label="") for i in range(8)] + [Group(i, label="") for i in ["a", "s", "d", "f"]]
'''
groups.append(
        ScratchPad("scratchpad", [
            DropDown("term", "alacritty", opacity=0.8, height=0.5, width=0.8),
            ]),
)

'''

for i in groups:
    keys.append(Key([mod], i.name, lazy.function(go_to_group(i.name))))
    keys.append(Key([mod, "shift"], i.name, lazy.function(go_to_group_and_move_window(i.name))))

# set correct group on screen
@hook.subscribe.startup
def set_screen_two_to_group_5():
    qtile.focus_screen(1)
    qtile.groups_map["5"].cmd_toscreen()
    qtile.focus_screen(0)

@hook.subscribe.startup
def set_screen_three_to_group_q():
    qtile.focus_screen(2)
    qtile.groups_map["a"].cmd_toscreen()
    qtile.focus_screen(0)

@hook.subscribe.startup
def set_screen_two_to_group_5():
    qtile.focus_screen(1)
    qtile.groups_map["5"].cmd_toscreen()
    qtile.focus_screen(0)

# Set correct layout on screens/groups
@hook.subscribe.startup
def set_MonadWide():
    if len(qtile.screens) == 3:
        for name in "1234":
            qtile.next_layout(name)
# Move windows across screens
@lazy.group.function
def send_to_next_screen(group):
    if group.name in "1234":
        qtile.focus_screen(1)
        active_group_on_next_screen = qtile.current_group
        qtile.focus_screen(0)
        qtile.current_window.cmd_togroup(active_group_on_next_screen.name, switch_group=False)
        qtile.focus_screen(1)
        qtile.groups_map[name].cmd_toscreen()
    elif group.name in "5678":
        qtile.focus_screen(2)
        active_group_on_next_screen = qtile.current_group
        qtile.focus_screen(1)
        qtile.current_window.cmd_togroup(active_group_on_next_screen.name, switch_group=False)
        qtile.focus_screen(2)
        qtile.groups_map[name].cmd_toscreen()
    else: 
        qtile.focus_screen(0)
        active_group_on_next_screen = qtile.current_group
        qtile.focus_screen(2)
        qtile.current_window.cmd_togroup(active_group_on_next_screen.name, switch_group=False)
        qtile.focus_screen(0)
        qtile.groups_map[name].cmd_toscreen()


keys.append(Key([mod], "o", send_to_next_screen()))
    
layouts = custom_layouts

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()
try: 
    if get_screens_connected() == 2: 
        #screens = [Screen(top=my_second_bar()), Screen(top=my_bar())]
        screens = [Screen(top=my_bar()), Screen(top=my_second_bar())]
    elif get_screens_connected() == 3: 
        screens = [Screen(top=my_third_bar()), Screen(top=my_bar()), Screen(top=my_second_bar())]
    else:
        screens = [Screen(top=my_bar())]
except Exception as e:
    logger.exception(str(e))

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
