import sqlite3
from pathlib import Path

from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldLeadingIcon,
    MDTextFieldHintText,
    MDTextFieldHelperText,
    MDTextFieldTrailingIcon,
    MDTextFieldMaxLengthText,
)
from kivymd.uix.textfield.textfield import Validator
from kivy.lang import Builder

from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)

import database

from kivy.metrics import dp, sp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage

def cargar_tareas(self):
    rows = database.read_tasks()

    container = self.root.ids.subscriptions_container

    container.clear_widgets()
    for id, descripcion, prioridad, fecha_limite, completado in rows:
        card = MDCard(
            style="elevated",
            size_hint_y=None,
            height=dp(100),
            radius=[20],
            padding=dp(16)
        )

        layout = MDBoxLayout(orientation="vertical", spacing=dp(6))
        card.add_widget(layout)

        layout.add_widget(
            MDLabel(
                text=f"[b]{descripcion}[/b]",
                halign="left",
                font_size=sp(18),
                markup=True,
                text_color=(0, 0, 0, 1)
            )
        )

        layout.add_widget(
            MDLabel(
                text=f"Fecha límite: {fecha_limite}",
                halign="left",
                font_size=sp(14),
                text_color=(0.3, 0.3, 0.3, 1)
            )
        )

        layout.add_widget(
            MDLabel(
                text=f"Prioridad: {prioridad}",
                halign="left",
                font_size=sp(14),
                text_color=(0.3, 0.3, 0.3, 1)
            )
        )

        container.add_widget(card)


class MainApp(MDApp):
    dialog = None

    def build(self):
        return Builder.load_file("main.kv")
    
    def on_start(self):
        database.create_db()
        cargar_tareas(self)
    
    def añadir_tarea(self):
        if not self.dialog:
            self.descripcion_dialog = MDTextField(
                MDTextFieldLeadingIcon(
                    icon="format-letter-case",
                ),
                MDTextFieldHintText(text="Tarea"),
                MDTextFieldMaxLengthText(max_text_length=64)
            )
            self.fecha_dialog = MDTextField(
                MDTextFieldLeadingIcon(
                    icon="calendar-range",
                ),
                MDTextFieldHintText(text="Fecha límite"),
                MDTextFieldMaxLengthText(max_text_length=16),
                MDTextFieldHelperText(text="DD/MM/AAAA")
            )
            self.prioridad = MDTextField(
                MDTextFieldLeadingIcon(
                    icon="star-check",
                ),
                MDTextFieldHintText(text="Prioridad"),
                MDTextFieldMaxLengthText(max_text_length=32)
            )

            self.dialog = MDDialog(
                MDDialogIcon(icon="new-box"),
                MDDialogHeadlineText(text="Nueva Tarea", halign="center"),
                MDDialogContentContainer(
                        self.descripcion_dialog,
                        self.fecha_dialog,
                        self.prioridad,
                        orientation="vertical",
                        spacing="32dp"
                ),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(
                        MDButtonText(text="Cancel"),
                        on_release=lambda *args: self.dialog.dismiss(),
                        style="text"
                    ),
                    MDButton(
                        MDButtonText(text="Add"),
                        on_release=self.guardar_tarea,
                        style="text"
                    ),
                    spacing="8dp",
                )
            )
        self.dialog.open()

    def guardar_tarea(self, *a):
        descripcion_dialog = self.descripcion_dialog.text.strip()
        fecha_dialog = self.fecha_dialog.text.strip()
        prioridad = self.prioridad.text.strip()

        database.create_task(descripcion_dialog, fecha_dialog, prioridad)
        cargar_tareas(self)

        self.dialog.dismiss()

MainApp().run()
