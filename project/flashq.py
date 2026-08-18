import flet as ft
import pandas as pd

def main(page: ft.Page):
    page.title = "flash"
    page.theme_mode = "dark"
    page.window_width = 800
    page.window_height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ALWAYS

    data_table = ft.DataTable(
        
        columns=[ft.DataColumn(ft.Text("Ожидание загрузки данных..."))],
        rows=[]     # Здесь будут данные (DataRow)
    )

    table_container = ft.Column(
        controls=[
            ft.Row([data_table], scroll=ft.ScrollMode.ALWAYS)
        ],
        scroll=ft.ScrollMode.ALWAYS,
        expand=True # Таблица занимает все свободное место
    )

    status_text = ft.Text("Выберите файл для отображения", color="grey")

    

    def pick_files(e: ft.ControlEvent):
        if not e.files:
            return
            
        filepath = e.files[0].path
        
        try:
            
            df = pd.read_html(filepath, encoding='utf-8')[0]
            df_display = df.head(50) #
            
           
            data_table.columns = [
                ft.DataColumn(ft.Text(str(col_name), weight="bold"))
                for col_name in df_display.columns
            ]
            
            
            rows = []
            for index, row in df_display.iterrows():
                cells = [ft.DataCell(ft.Text(str(value))) for value in row]
                rows.append(ft.DataRow(cells=cells))
                
            data_table.rows = rows
            
        except Exception as ex:
            print(f"\n--- ОШИБКА ПРИ ЧТЕНИИ: {ex} ---\n")
        page.update()

    pick_dialog = ft.FilePicker()
    pick_dialog.on_result = pick_files
    page.overlay.append(pick_dialog)


    edit_dialog = ft.AlertDialog(
        title=ft.Text ('Зміна'),
        content=ft.TextField (label = 'ТЕСТ')
    )

    def change_file (e):
        page.open(edit_dialog)
        page.update()

    



        ft.Row ([
              ft.IconButton(
                icon=ft.icons.FOLDER_OPEN,
                on_click=lambda _: pick_dialog.pick_files(allow_multiple=False)
            ),
                 table_container]),
        
        
        
    
                            
      
    select_title = ft.Text()

    
    page.appbar = ft.AppBar(
    select_title,       
    center_title=True,       
    actions=[                 
        ft.IconButton(
            icon=ft.icons.FOLDER_OPEN,
            on_click=lambda _: pick_dialog.pick_files(allow_multiple=False),
            
        )
    ]
    
    )
    page.bottom_appbar =ft.BottomAppBar(
        bgcolor=ft.colors.SURFACE_VARIANT,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.IconButton(ft.icons.MENU),
                ft.IconButton(ft.icons.SEARCH),
                ft.IconButton(ft.icons.SETTINGS),
            ],
        ),
    )
        

    def navigate(e):
         # (0 - ТОТАЛ, 1 - ДОЖИМ)
      
        page.update()

    content_tabs = ft.Tabs(
    selected_index=0,
    animation_duration=300,
    tabs=[
        ft.Tab(text="ТОТАЛ"),
        ft.Tab(text="ДОЖИМ"),
    ],
    on_change=navigate)
    centered_tabs = ft.Row(
    controls=[content_tabs],
    alignment=ft.MainAxisAlignment.CENTER
)



    
    page.add(centered_tabs, table_container )
ft.app(main)