from __future__ import annotations

from kivy.config import Config

# ─────────────────────────────────────────────────────────────
# GLOBALNE USTAWIENIA OKNA
# ─────────────────────────────────────────────────────────────
APP_WIDTH = 350
APP_HEIGHT = 735

Config.set("graphics", "width", str(APP_WIDTH))
Config.set("graphics", "height", str(APP_HEIGHT))

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from sympy_basic_parser import calculate


# ─────────────────────────────────────────────────────────────
# KOLORY
# ─────────────────────────────────────────────────────────────
PALETTE = {
    "screen": (28 / 255, 31 / 255, 43 / 255, 1),
    "keyboard": (18 / 255, 18 / 255, 18 / 255, 1),
    "digit": (34 / 255, 35 / 255, 38 / 255, 1),
    "digit_down": (45 / 255, 46 / 255, 50 / 255, 1),
    "op": (64 / 255, 70 / 255, 89 / 255, 1),
    "op_down": (45 / 255, 50 / 255, 69 / 255, 1),
    "utility": (81 / 255, 63 / 255, 102 / 255, 1),
    "utility_down": (82 / 255, 54 / 255, 90 / 255, 1),
    "accent": (67 / 255, 72 / 255, 117 / 255, 1),
    "accent_down": (84 / 255, 89 / 255, 140 / 255, 1),
    "text": (1, 1, 1, 1),
    "screen_text": (242 / 255, 246 / 255, 255 / 255, 1),
}

WINDOW_BG = (0.07058823529411765, 0.07058823529411765, 0.07058823529411765, 1)
Window.clearcolor = WINDOW_BG


# ─────────────────────────────────────────────────────────────
# KONFIGURACJA UI
# ─────────────────────────────────────────────────────────────
class UI:
    # Root
    ROOT_PADDING = [dp(0), dp(0), dp(0), dp(0)] #14, 24, 14, 14
    ROOT_SPACING = dp(0) #12

    # Ekran
    DISPLAY_PANEL_RADIUS = dp(0) #26
    DISPLAY_PANEL_HEIGHT = dp(200) #190
    DISPLAY_PANEL_PADDING = dp(18) #18
    DISPLAY_PANEL_SPACING = dp(4) #4

    DISPLAY_FONT_SIZE = dp(28) #28
    RESULT_FONT_SIZE = dp(40) #40
    RESULT_HEIGHT = dp(30) #35

    INPUT_FONT_SIZE = dp(30)
    INPUT_PADDING = [dp(12), dp(10), dp(12), dp(10)]
    INPUT_HEIGHT = dp(58)
    INPUT_CURSOR_WIDTH = dp(2)

    # Klawiatura
    KEYBOARD_PANEL_RADIUS = dp(0) #28
    KEYBOARD_PANEL_PADDING = dp(2) #12
    KEYBOARD_PANEL_SPACING = dp(0) #6
    GRID_SPACING = dp(6) #6

    # Główne przyciski
    MAIN_BTN_NORMAL = (dp(75), dp(75))
    MAIN_BTN_EXPANDED = (dp(70), dp(58))
    MAIN_BTN_FONT_SIZE = dp(24)

    # Dodatkowe przyciski
    EXTRA_BTN_SIZE = (dp(70), dp(36))
    EXTRA_BTN_FONT_SIZE = dp(18)

    # Zakładki
    PAGE_BTN_SIZE = (dp(70), dp(36))
    PAGE_BTN_FONT_SIZE = dp(14)
    PAGE_BAR_HEIGHT = dp(34)

    # Przycisk rozwijania
    EXPAND_BTN_SIZE = (dp(20), dp(20))
    EXPAND_BTN_FONT_SIZE = dp(14)

    # Animacje
    BTN_ANIM_NORMAL = 0.12
    BTN_ANIM_EXPAND = 0.20
    EXTRA_PANEL_ANIM = 0.22

    # Dół głównej siatki
    MAIN_GRID_BOTTOM_PADDING = dp(100) #80

    # Promienie
    BUTTON_RADIUS_SMALL = dp(10)
    BUTTON_RADIUS_BASE = dp(12)


# ─────────────────────────────────────────────────────────────
# UKŁADY PRZYCISKÓW
# ─────────────────────────────────────────────────────────────
MAIN_LAYOUT = [
    [("(", "op"), (")", "op"), ("^", "op"), ("rt", "op")],
    [("CA", "utility"), ("<-", "op"), ("->", "op"), ("÷", "op")],
    [("7", "digit"), ("8", "digit"), ("9", "digit"), ("×", "op")],
    [("4", "digit"), ("5", "digit"), ("6", "digit"), ("−", "op")],
    [("1", "digit"), ("2", "digit"), ("3", "digit"), ("+", "op")],
    [("0", "digit"), (",", "digit"), ("DEL", "digit"), ("=", "accent")],
]

PAGE_LAYOUTS = {
    "trig": [
        ("sin", "keyboard"), ("cos", "keyboard"), ("tan", "keyboard"), ("π", "keyboard"),
        ("asin", "keyboard"), ("acos", "keyboard"), ("atan", "keyboard"), ("e", "keyboard"),
    ],
    "log": [
        ("log", "op"), ("ln", "op"), ("10^", "op"), ("e^", "op"),
        ("x²", "utility"), ("x³", "utility"), ("|x|", "utility"), ("1/x", "utility"),
    ],
    "eq": [
        ("=", "accent"), ("<", "op"), (">", "op"), ("≤", "op"),
        ("≥", "op"), ("≠", "op"), ("solve", "utility"), ("x", "utility"),
    ],
    "misc": [
        ("%", "op"), ("!", "op"), ("rand", "utility"), ("ans", "utility"),
        ("deg", "utility"), ("rad", "utility"), ("exp", "utility"), ("π", "utility"),
    ],
}


# ─────────────────────────────────────────────────────────────
# KOMPONENTY
# ─────────────────────────────────────────────────────────────
class Panel(BoxLayout):
    def __init__(self, bg=(1, 1, 1, 1), radius=dp(24), **kwargs):
        super().__init__(**kwargs)
        self.bg = bg
        self.radius = radius
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])


class RoundedRectButton(Button):
    def __init__(self, kind: str = "digit", **kwargs):
        super().__init__(**kwargs)
        self.kind = kind
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = PALETTE["text"]
        self.font_size = UI.MAIN_BTN_FONT_SIZE
        self.bold = False
        self.size_hint = (None, None)
        self.size = (dp(40), dp(40))
        self.halign = "center"
        self.valign = "middle"
        self.text_size = self.size
        self.bind(pos=self._redraw, size=self._redraw)
        self.bind(size=lambda inst, *_: setattr(inst, "text_size", inst.size))
        self.bind(state=self._redraw)

    def _bg(self):
        base = PALETTE.get(self.kind, PALETTE["digit"])
        if self.state == "down":
            return PALETTE.get(f"{self.kind}_down", base)
        return base

    def _radius(self):
        w, h = self.size
        if self.height <= dp(42):
            return [UI.BUTTON_RADIUS_SMALL]
        if abs(w - h) < 1e-6:
            return [w / 2]
        return [max(UI.BUTTON_RADIUS_BASE, min(h * 0.46, w * 0.34))]

    def _redraw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self._bg())
            RoundedRectangle(pos=self.pos, size=self.size, radius=self._radius())


class ExpressionField(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.readonly = False
        self.font_size = UI.INPUT_FONT_SIZE
        self.halign = "right"
        self.valign = "middle"
        self.cursor_blink = True
        self.cursor_width = UI.INPUT_CURSOR_WIDTH
        self.cursor_color = PALETTE["screen_text"]
        self.foreground_color = PALETTE["screen_text"]
        self.background_color = (0, 0, 0, 0)
        self.padding = UI.INPUT_PADDING
        self.size_hint_y = None
        self.height = UI.INPUT_HEIGHT
        self.write_tab = False
        self.auto_indent = False
        self.use_handles = False
        self.bind(focus=self._ensure_cursor_visible)

    def _ensure_cursor_visible(self, *_):
        if self.focus:
            self.cursor_blink = True


# ─────────────────────────────────────────────────────────────
# ROOT
# ─────────────────────────────────────────────────────────────
class CalculatorRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = UI.ROOT_PADDING
        self.spacing = UI.ROOT_SPACING

        self.expanded = False
        self.active_page = "trig"

        self.grid = None
        self.extra_grid = None
        self.main_container = None
        self.extra_container = None
        self.main_buttons: list[RoundedRectButton] = []
        self.extra_buttons: list[RoundedRectButton] = []
        self.page_buttons: dict[str, RoundedRectButton] = {}

        self._build_display_area()
        self._build_keyboard_area()

        self.display.bind(text=self._update_live_result)
        Clock.schedule_once(lambda dt: setattr(self.display, "focus", True), 0)
        self.bind(size=self._schedule_reflow)

    def _schedule_reflow(self, *_):
        Clock.schedule_once(self._reflow_keyboard, 0)

    def _build_display_area(self):
        self.display_panel = Panel(
            bg=PALETTE["screen"],
            radius=UI.DISPLAY_PANEL_RADIUS,
            size_hint_y=None,
            height=UI.DISPLAY_PANEL_HEIGHT,
            padding=UI.DISPLAY_PANEL_PADDING,
        )
        self.display_panel.orientation = "vertical"
        self.display_panel.spacing = UI.DISPLAY_PANEL_SPACING

        self.display = ExpressionField(text="", font_size=UI.DISPLAY_FONT_SIZE)
        self.display.bind(size=lambda inst, *_: setattr(inst, "text_size", (inst.width - dp(24), None)))

        self.result = Label(
            text="",
            font_size=UI.RESULT_FONT_SIZE,
            color=PALETTE["screen_text"],
            halign="right",
            valign="middle",
            size_hint_y=None,
            height=UI.RESULT_HEIGHT,
        )
        self.result.bind(size=lambda inst, *_: setattr(inst, "text_size", inst.size))

        bottom_bar = BoxLayout(size_hint_y=None, height=dp(34))
        expand_btn = RoundedRectButton(
            text="⋯",
            kind="op",
            size=UI.EXPAND_BTN_SIZE,
            font_size=UI.EXPAND_BTN_FONT_SIZE,
        )
        expand_btn.bind(on_press=self.toggle_expand)
        bottom_bar.add_widget(expand_btn)
        bottom_bar.add_widget(BoxLayout())

        self.display_panel.add_widget(self.display)
        self.display_panel.add_widget(self.result)
        self.display_panel.add_widget(bottom_bar)
        self.add_widget(self.display_panel)

    def _build_keyboard_area(self):
        self.keyboard_panel = Panel(
            bg=PALETTE["keyboard"],
            radius=UI.KEYBOARD_PANEL_RADIUS,
            padding=UI.KEYBOARD_PANEL_PADDING,
            size_hint_y=1,
        )
        self.keyboard_panel.orientation = "vertical"
        self.keyboard_panel.spacing = UI.KEYBOARD_PANEL_SPACING

        self.extra_container = BoxLayout(size_hint_y=None, height=0, opacity=0, disabled=True)
        self.extra_container.orientation = "vertical"
        self.extra_container.spacing = UI.KEYBOARD_PANEL_SPACING

        self.page_bar = BoxLayout(size_hint_y=None, height=UI.PAGE_BAR_HEIGHT, spacing=UI.GRID_SPACING)
        for page, label in [("trig", "Trig"), ("log", "Log"), ("eq", "Eq"), ("misc", "More")]:
            btn = RoundedRectButton(text=label, kind="op", font_size=UI.PAGE_BTN_FONT_SIZE)
            btn.size = self._page_dims()
            btn.bind(on_press=self.set_page)
            self.page_buttons[page] = btn
            self.page_bar.add_widget(btn)

        self.extra_anchor = AnchorLayout(anchor_x="center", anchor_y="center")
        self.extra_grid = GridLayout(
            cols=4,
            spacing=UI.GRID_SPACING,
            size_hint=(None, None),
            row_force_default=True,
            col_force_default=True,
            row_default_height=UI.EXTRA_BTN_SIZE[1],
            col_default_width=UI.EXTRA_BTN_SIZE[0],
        )
        self.extra_anchor.add_widget(self.extra_grid)

        self.extra_container.add_widget(self.page_bar)
        self.extra_container.add_widget(self.extra_anchor)

        self.main_container = BoxLayout(size_hint_y=1, padding=[0, dp(8), 0, UI.MAIN_GRID_BOTTOM_PADDING])
        self.main_anchor = AnchorLayout(anchor_x="center", anchor_y="center")
        self.grid = GridLayout(
            cols=4,
            spacing=UI.GRID_SPACING,
            size_hint=(None, None),
            row_force_default=True,
            col_force_default=True,
            row_default_height=UI.MAIN_BTN_NORMAL[1],
            col_default_width=UI.MAIN_BTN_NORMAL[0],
        )
        self.main_anchor.add_widget(self.grid)
        self.main_container.add_widget(self.main_anchor)

        self.keyboard_panel.add_widget(self.extra_container)
        self.keyboard_panel.add_widget(self.main_container)
        self.add_widget(self.keyboard_panel)

        for row in MAIN_LAYOUT:
            for label, kind in row:
                btn = RoundedRectButton(text=label, kind=kind)
                btn.bind(on_press=self.on_button)
                self.main_buttons.append(btn)
                self.grid.add_widget(btn)

        self._build_extra_buttons()
        self._refresh_page()
        Clock.schedule_once(self._reflow_keyboard, 0)

    def _build_extra_buttons(self):
        if self.extra_buttons:
            return

        for _ in range(12):
            btn = RoundedRectButton(text="", kind="op", font_size=UI.EXTRA_BTN_FONT_SIZE)
            btn.size = self._page_dims()
            btn.bind(on_press=self.on_button)
            self.extra_buttons.append(btn)
            self.extra_grid.add_widget(btn)

    def _page_dims(self):
        if self.expanded:
            return UI.PAGE_BTN_SIZE
        return UI.PAGE_BTN_SIZE

    def _page_layout(self):
        return PAGE_LAYOUTS

    def _refresh_page(self):
        items = self._page_layout().get(self.active_page, [])
        page_w, page_h = self._page_dims()

        for btn, (label, kind) in zip(self.extra_buttons, items):
            btn.text = label
            btn.kind = kind
            btn.size = (page_w, page_h)
            btn.disabled = False
            btn.opacity = 1

        for btn in self.extra_buttons[len(items):]:
            btn.text = ""
            btn.disabled = True
            btn.opacity = 0

        for page, btn in self.page_buttons.items():
            btn.kind = "keyboard" if page == self.active_page else "keyboard"
            btn.size = self._page_dims()

    def set_page(self, instance):
        label_map = {btn.text: page for page, btn in self.page_buttons.items()}
        self.active_page = label_map.get(instance.text, "trig")
        self._refresh_page()

    def _update_live_result(self, *_):
        expr = self.display.text.strip()
        if not expr:
            self.result.text = ""
            return
        try:
            self.result.text = calculate(expr).exact_text
        except Exception:
            self.result.text = ""

    def _set_cursor_index(self, index: int):
        index = max(0, min(index, len(self.display.text)))
        self.display.focus = True
        Clock.schedule_once(
            lambda dt: setattr(self.display, "cursor", self.display.get_cursor_from_index(index)),
            0,
        )

    def _main_dims(self) -> tuple[float, float]:
        return UI.MAIN_BTN_EXPANDED if self.expanded else UI.MAIN_BTN_NORMAL

    def _extra_dims(self) -> tuple[float, float]:
        return UI.EXTRA_BTN_SIZE

    def _animate_button_group(self, buttons: list[RoundedRectButton], width: float, height: float, d: float):
        for btn in buttons:
            Animation.cancel_all(btn)
            Animation(size=(width, height), d=d, t="out_quad").start(btn)

    def _apply_grid_geometry(self):
        main_w, main_h = self._main_dims()
        extra_w, extra_h = self._extra_dims()
        gap = UI.GRID_SPACING

        self.grid.col_default_width = main_w
        self.grid.row_default_height = main_h
        self.grid.width = 4 * main_w + 3 * gap
        self.grid.height = 5 * main_h + 4 * gap

        if self.expanded and self.extra_buttons:
            self.extra_grid.col_default_width = extra_w
            self.extra_grid.row_default_height = extra_h
            self.extra_grid.width = 4 * extra_w + 3 * gap
            self.extra_grid.height = 3 * extra_h + 2 * gap
            self.extra_container.height = self.page_bar.height + self.extra_grid.height + gap
        else:
            self.extra_container.height = 0

    def _reflow_keyboard(self, *_):
        self._apply_grid_geometry()
        main_w, main_h = self._main_dims()
        page_w, page_h = self._page_dims()
        self._animate_button_group(self.main_buttons, main_w, main_h, d=UI.BTN_ANIM_NORMAL)
        self._animate_button_group(list(self.page_buttons.values()), page_w, page_h, d=UI.BTN_ANIM_NORMAL)
        if self.expanded and self.extra_buttons:
            self._animate_button_group(self.extra_buttons, *self._extra_dims(), d=UI.BTN_ANIM_NORMAL)
            self.extra_container.opacity = 1
            self.extra_container.disabled = False
        else:
            self.extra_container.opacity = 0
            self.extra_container.disabled = True

    def toggle_expand(self, *_):
        self.expanded = not self.expanded

        if self.expanded:
            self._animate_button_group(self.main_buttons, *self._main_dims(), d=UI.BTN_ANIM_EXPAND)
            self._animate_button_group(list(self.page_buttons.values()), *self._page_dims(), d=UI.BTN_ANIM_EXPAND)
            self._animate_button_group(self.extra_buttons, *self._extra_dims(), d=UI.BTN_ANIM_EXPAND)
            self.extra_container.disabled = False
            Animation(
                height=self.page_bar.height + self._extra_dims()[1] * 3 + dp(6) * 3,
                opacity=1,
                d=UI.EXTRA_PANEL_ANIM,
                t="out_cubic",
            ).start(self.extra_container)
        else:
            self._animate_button_group(self.main_buttons, *self._main_dims(), d=UI.BTN_ANIM_EXPAND)
            self._animate_button_group(list(self.page_buttons.values()), *self._page_dims(), d=UI.BTN_ANIM_EXPAND)
            Animation(height=0, opacity=0, d=UI.EXTRA_PANEL_ANIM, t="out_cubic").start(self.extra_container)
            self.extra_container.disabled = True

        Clock.schedule_once(self._reflow_keyboard, 0)

    def _insert_text(self, t: str):
        pos = self.display.cursor_index()
        text = self.display.text
        self.display.text = text[:pos] + t + text[pos:]
        self._set_cursor_index(pos + len(t))

    def on_button(self, instance):
        t = instance.text
        self.display.focus = True
        pos = self.display.cursor_index()
        text = self.display.text

        if t == "CA":
            self.display.text = ""
            self.result.text = ""
            self._set_cursor_index(0)
            return

        if t == "DEL":
            if pos > 0:
                self.display.text = text[:pos - 1] + text[pos:]
                self._set_cursor_index(pos - 1)
            return

        if t == "<-":
            if pos > 0:
                self._set_cursor_index(pos - 1)
            return

        if t == "->":
            if pos < len(text):
                self._set_cursor_index(pos + 1)
            return

        if t == "=":
            try:
                res = calculate(self.display.text)
                self.result.text = res.exact_text
            except Exception:
                self.result.text = "ERROR"
            return

        if t == ",":
            t = "."

        if t == "π":
            t = "pi"

        if t == "√":
            t = "sqrt("

        if t == "x²":
            t = "**2"

        if t == "x³":
            t = "**3"

        if t == "1/x":
            t = "1/("

        if t == "10^":
            t = "10**"

        if t == "e^":
            t = "E**"

        if t == "|x|":
            t = "Abs("

        if t == "ans":
            if self.result.text:
                t = self.result.text
            else:
                return

        if t in {"sin", "cos", "tan", "asin", "acos", "atan", "log", "ln", "exp", "solve"}:
            t += "("

        if t == "%":
            t = "/100"

        if t == "!":
            t = "!"

        if t == "rand":
            t = "Rational(1,2)"

        if t == "deg":
            t = "deg"

        if t == "rad":
            t = "rad"

        self._insert_text(t)


class CalculatorApp(App):
    def build(self):
        return CalculatorRoot()


if __name__ == "__main__":
    CalculatorApp().run()