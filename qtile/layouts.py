from libqtile import layout
from colors import colors

BORDER_WIDTH = 2
MARGIN = 9
SMART_GAPS = False

WINDOW_MARGIN = MARGIN  # int(MARGIN/2)

# width of the border of selected window if it's the only window in a group
# only used by monad wide and monad tall
SINGLE_BORDER_WIDTH = BORDER_WIDTH

ACTIVE_COLOR = colors["cyan"]

floating = layout.Floating(
    border_focus=ACTIVE_COLOR, border_width=2
)

monadwide = layout.MonadWide(
    border_focus=ACTIVE_COLOR,
    border_width=BORDER_WIDTH,
    margin=WINDOW_MARGIN,
)


monadtall = layout.MonadTall(
    border_focus=ACTIVE_COLOR,
    border_width=BORDER_WIDTH,
    margin=WINDOW_MARGIN,
)

_max = layout.Max(
    border_focus=ACTIVE_COLOR,
    border_width=BORDER_WIDTH,
    margin=WINDOW_MARGIN,
)

stack = layout.Stack(
    border_focus=ACTIVE_COLOR,
    border_width=BORDER_WIDTH,
    margin=WINDOW_MARGIN,
)

tree = layout.TreeTab(
    border_focus=ACTIVE_COLOR,
    border_width=BORDER_WIDTH,
    margin=WINDOW_MARGIN,
)

custom_layouts = [monadtall, monadwide, stack, tree, _max, floating]
