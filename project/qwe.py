import flet as ft

def main(page: ft.Page):
    page.title = "flash"
    page.theme_mode = "dark"
    page.window_width = 400
    page.window_height = 500
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def pick_files(e: ft.ControlEvent):
        if e.files:
            selected_files.value = f"Обрано: {e.files[0].name}"
        else:
            selected_files.value = "Вибір скасовано"
        page.update()

    pick_dialog = ft.FilePicker()
    pick_dialog.on_result = pick_files
    page.overlay.append(pick_dialog)

    selected_files = ft.Text()

    page.add(
        ft.Row([ft.Text('тест')]),
        ft.Row([
            ft.Button(
                'Оберіть файл',
                icon="folder_open",
                on_click=lambda _: pick_dialog.pick_files(allow_multiple=False)
            )
        ]),
        ft.Row([selected_files])
    )

ft.app(main)