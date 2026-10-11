from __future__ import annotations

import tkinter as tk
from abc import ABC, abstractmethod
from typing import Callable, Optional


PARENT_BG = "#f4f4f5"
FIELD_BG = "#ffffff"
BLUE_BORDER = "#2563eb"
RED_BORDER = "#dc2626"


class InputState(ABC):
    name: str

    # ---- Singleton: cada subclasse concreta (NormalState, FocusState,
    # ErrorState) terá exatamente UMA instância, reaproveitada sempre. ----
    _instance: Optional["InputState"] = None

    @classmethod
    def instance(cls) -> "InputState":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @abstractmethod
    def apply(self, field: "StatefulEntry") -> None:
        ...

    def on_focus_in(self, field: "StatefulEntry") -> None:
        field.set_state(FocusState.instance())

    def on_focus_out(self, field: "StatefulEntry") -> None:
        field.set_state(NormalState.instance())

    def on_error(self, field: "StatefulEntry") -> None:
        field.set_state(ErrorState.instance())

    def on_clear_error(self, field: "StatefulEntry") -> None:
        if field.has_focus():
            field.set_state(FocusState.instance())
        else:
            field.set_state(NormalState.instance())


class NormalState(InputState):
    name = "normal"

    def apply(self, field: "StatefulEntry") -> None:
        field.set_border(PARENT_BG, thickness=0)


class FocusState(InputState):
    name = "focus"

    def apply(self, field: "StatefulEntry") -> None:
        field.set_border(BLUE_BORDER, thickness=2)

    def on_focus_in(self, field: "StatefulEntry") -> None:
        return


class ErrorState(InputState):
    name = "error"

    def apply(self, field: "StatefulEntry") -> None:
        field.set_border(RED_BORDER, thickness=2)

    def on_focus_in(self, field: "StatefulEntry") -> None:
        return

    def on_focus_out(self, field: "StatefulEntry") -> None:
        return


class StatefulEntry(tk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        on_state_change: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            bg=PARENT_BG,
            highlightthickness=0,
            highlightbackground=PARENT_BG,
            highlightcolor=PARENT_BG,
        )

        # callback opcional chamado sempre que o estado mudar de verdade,
        # em vez de alguém precisar ficar perguntando "qual é o estado?" (polling)
        self._on_state_change = on_state_change

        self._entry = tk.Entry(
            self,
            bd=0,
            relief=tk.FLAT,
            bg=FIELD_BG,
            fg="#111827",
            insertbackground="#111827",
            font=("Segoe UI", 12),
            **kwargs,
        )
        self._entry.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self._state: InputState = NormalState.instance()
        self._state.apply(self)

        self._entry.bind("<FocusIn>", self._handle_focus_in)
        self._entry.bind("<FocusOut>", self._handle_focus_out)
        self._entry.bind("<KeyRelease>", self._handle_key_release)

    def set_state(self, state: InputState) -> None:
        self._state = state
        self._state.apply(self)
        if self._on_state_change is not None:
            self._on_state_change(self._state.name)

    def set_border(self, color: str, thickness: int) -> None:
        self.configure(
            highlightthickness=thickness,
            highlightbackground=color,
            highlightcolor=color,
        )

    def get(self) -> str:
        return self._entry.get().strip()

    def has_focus(self) -> bool:
        return self.focus_get() is self._entry

    def state_name(self) -> str:
        # ponto de acesso público ao estado atual, sem expor o atributo _state
        return self._state.name

    def show_error(self) -> None:
        self._state.on_error(self)

    def _handle_focus_in(self, _event: tk.Event) -> None:
        self._state.on_focus_in(self)

    def _handle_focus_out(self, _event: tk.Event) -> None:
        self._state.on_focus_out(self)

    def _handle_key_release(self, _event: tk.Event) -> None:
        if isinstance(self._state, ErrorState) and self.get():
            self._state.on_clear_error(self)


def build_demo() -> tk.Tk:
    root = tk.Tk()
    root.title("Input field states")
    root.configure(bg=PARENT_BG)
    root.geometry("420x220")
    root.resizable(False, False)

    status = tk.StringVar(value="Status: normal")

    def update_status(state_name: str) -> None:
        # chamado diretamente pela StatefulEntry quando o estado muda de
        # verdade - sem loop, sem polling, sem checar a cada 80ms
        status.set(f"Status: {state_name}")

    label = tk.Label(
        root,
        text="Name",
        bg=PARENT_BG,
        fg="#374151",
        font=("Segoe UI", 11),
        anchor="w",
    )
    label.pack(fill=tk.X, padx=24, pady=(28, 6))

    field = StatefulEntry(root, on_state_change=update_status)
    field.pack(fill=tk.X, padx=24)

    hint = tk.Label(
        root,
        textvariable=status,
        bg=PARENT_BG,
        fg="#6b7280",
        font=("Segoe UI", 10),
        anchor="w",
    )
    hint.pack(fill=tk.X, padx=24, pady=(8, 0))

    def validate() -> None:
        if not field.get():
            field.show_error()
        else:
            field.set_state(
                NormalState.instance() if not field.has_focus() else FocusState.instance()
            )

    submit = tk.Button(
        root,
        text="Validate",
        command=validate,
        bd=0,
        padx=16,
        pady=6,
        bg="#111827",
        fg="#ffffff",
        activebackground="#1f2937",
        activeforeground="#ffffff",
        font=("Segoe UI", 10),
        cursor="hand2",
    )
    submit.pack(anchor="e", padx=24, pady=20)

    return root


if __name__ == "__main__":
    app = build_demo()
    app.mainloop()