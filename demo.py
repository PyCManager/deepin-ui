#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import skin and theme, those must before at any other modules.
# from skin import ui_theme, app_theme
from dtk.ui.skin_config import skin_config
from dtk.ui.theme import Theme, ui_theme
from dtk.ui.utils import get_parent_dir
import os

# Init skin config.
skin_config.init_skin(
    "01",
    os.path.join(get_parent_dir(__file__), "skin"),
    os.path.expanduser("~/.config/deepin-demo/skin"),
    os.path.expanduser("~/.config/deepin-demo/skin_config.ini"),
    )

# Create application theme.
app_theme = Theme(
    os.path.join(get_parent_dir(__file__), "app_theme"),
    os.path.expanduser("~/.config/deepin-demo/theme")
    )

# Set theme.
skin_config.load_themes(ui_theme, app_theme)

# Load other modules.
from dtk.ui.application import Application
from dtk.ui.button import ImageButton
from dtk.ui.categorybar import Categorybar
from dtk.ui.constant import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, WIDGET_POS_BOTTOM_LEFT
from dtk.ui.entry import TextEntry, ShortcutKeyEntry
from dtk.ui.frame import HorizontalFrame
from dtk.ui.group import ImageButtonGroup, ToggleButtonGroup
from dtk.ui.label import Label
from dtk.ui.listview import ListItem, ListView
from dtk.ui.droplist import Droplist
from dtk.ui.menu import Menu
from dtk.ui.treeview import TreeView, TreeViewItem
from dtk.ui.navigatebar import Navigatebar
from dtk.ui.notebook import Notebook
from dtk.ui.popup_window import PopupWindow
from dtk.ui.tab_window import TabWindow
from dtk.ui.color_selection import ColorButton
from dtk.ui.scalebar import HScalebar, VScalebar
from dtk.ui.scrolled_window import ScrolledWindow
from dtk.ui.statusbar import Statusbar
from dtk.ui.tooltip import Tooltip
from dtk.ui.utils import container_remove_all, get_widget_root_coordinate
from dtk.ui.volume_button import VolumeButton
from dtk.ui.iconview import IconView, IconItem
from dtk.ui.paned import HPaned
from dtk.ui.button import CheckButton, RadioButton
from dtk.ui.combo import ComboBox
from dtk.ui.spin import SpinBox
from dtk.ui.textview import TextView
from dtk.ui.unique_service import UniqueService, is_exists
from dtk.ui.browser import WebView
import sys
import gtk
import dbus
import dbus.service
import time

def print_button_press(list_view, list_item, column, offset_x, offset_y):
    '''Print button press.'''
    print "* Button press: %s" % (str((list_item.title, list_item.artist, list_item.length)))

def print_double_click(list_view, list_item, column, offset_x, offset_y):
    '''Print double click.'''
    print "* Double click: %s" % (str((list_item.title, list_item.artist, list_item.length)))
    list_view.set_highlight(list_item)

def print_single_click(list_view, list_item, column, offset_x, offset_y):
    '''Print single click.'''
    print "* Single click: %s" % (str((list_item.title, list_item.artist, list_item.length)))
    list_view.clear_highlight()

def print_motion_notify(list_view, list_item, column, offset_x, offset_y):
    '''Print motion notify.'''
    print "* Motion notify: %s" % (str((list_item.title, list_item.artist, list_item.length, column, offset_x, offset_y)))
    
def print_entry_action(entry, entry_text):
    '''Print entry action.'''
    print entry_text
    
def simulate_redraw_request(items, items_length):
    '''Simulate item's redraw request.'''
    item_index = int(time.time() * 100) % items_length
    print items[item_index].length
    items[item_index].emit_redraw_request()
    
    return True

def switch_tab(notebook_box, tab_box):
    '''Switch tab 1.'''
    if not tab_box in notebook_box.get_children():
        container_remove_all(notebook_box)
        notebook_box.add(tab_box)
    
        notebook_box.show_all()
        
def create_tab_window_item(name):
    '''docs'''
    align = gtk.Alignment()
    align.set(0.5, 0.5, 0.0, 0.0)
    align.add(gtk.Button(name))
    
    return (name, align)
    
if __name__ == "__main__":
    # Build DBus name.
    app_dbus_name = "com.deepin.demo"
    app_object_name = "/com/deepin/demo"
    
    # Check unique.
    if is_exists(app_dbus_name, app_object_name):
        sys.exit()
    
    # Init application.
    application = Application()
    
    # Startup unique service, must after application code.
    app_bus_name = dbus.service.BusName(app_dbus_name, bus=dbus.SessionBus())
    UniqueService(app_bus_name, app_dbus_name, app_object_name, application.raise_to_top)
    
    # Set application default size.
    application.set_default_size(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
    
    # Set application icon.
    application.set_icon(ui_theme.get_pixbuf("icon.ico"))
    
    # Set application preview pixbuf.
    application.set_skin_preview(app_theme.get_pixbuf("frame.png"))
    
    # Add titlebar.
    application.add_titlebar(
        ["theme", "menu", "max", "min", "close"], 
        ui_theme.get_pixbuf("logo.png"), 
        "深度图形库",
        "/home/andy/deepin-ui/loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooony.py")
    
    # Draw application background.
    button = gtk.Button()
    button.set_size_request(200,300)
    
    # Init menu callback.
    sub_menu_a = Menu(
        [(None, "子菜单A1", None),
         None,
         (None, "子菜单A2", None),
         (None, "子菜单A3", None),
         ])
    sub_menu_e = Menu(
        [(None, "子菜单E1", None),
         (None, "子菜单E2", None),
         None,
         (None, "子菜单E3", None),
         ])
    sub_menu_d = Menu(
        [(None, "子菜单D1", None),
         (None, "子菜单D2", None),
         None,
         (None, "子菜单D3", sub_menu_e),
         ])
    sub_menu_c = Menu(
        [(None, "子菜单C1", None),
         (None, "子菜单C2", None),
         None,
         (None, "子菜单C3", sub_menu_d),
         ])
    sub_menu_b = Menu(
        [(None, "子菜单B1", None),
         None,
         (None, "子菜单B2", None),
         None,
         (None, "子菜单B3", sub_menu_c),
         ])
    
    menu = Menu(
        [((ui_theme.get_pixbuf("menu/item1_normal.png"), ui_theme.get_pixbuf("menu/item1_hover.png")),
          "测试测试测试1", lambda : PopupWindow(application.window)),
         ((ui_theme.get_pixbuf("menu/item2_normal.png"), ui_theme.get_pixbuf("menu/item2_hover.png")),
          "测试测试测试2", sub_menu_a),
         ((ui_theme.get_pixbuf("menu/item3_normal.png"), ui_theme.get_pixbuf("menu/item3_hover.png")),
          "测试测试测试3", sub_menu_b),
         ((ui_theme.get_pixbuf("menu/item4_normal.png"), ui_theme.get_pixbuf("menu/item4_hover.png")),
          "测试测试测试", None),
         ((ui_theme.get_pixbuf("menu/item5_normal.png"), ui_theme.get_pixbuf("menu/item5_hover.png")),
          "测试测试测试", None),
         ((ui_theme.get_pixbuf("menu/item6_normal.png"), ui_theme.get_pixbuf("menu/item6_hover.png")),
          "测试测试测试4", None, (1, 2, 3)),
         ((ui_theme.get_pixbuf("menu/item7_normal.png"), ui_theme.get_pixbuf("menu/item7_hover.png")),
          "测试测试测试5", None),
         ((ui_theme.get_pixbuf("menu/item8_normal.png"), ui_theme.get_pixbuf("menu/item8_hover.png")),
          "测试测试测试6", None),
         ],
        True
        )
    application.set_menu_callback(lambda button: menu.show(
            get_widget_root_coordinate(button, WIDGET_POS_BOTTOM_LEFT),
            (button.get_allocation().width, 0)))
    
    # Add navigatebar.
    tab_window_items = map(create_tab_window_item, ["Tab1", "Tab2", "Tab3", "Tab4", "Tab5"])
    
    droplist = Droplist(
        [("测试测试测试1", None),
         ("测试测试测试2", None),
         ("测试测试测试3", None),
         None,
         ("测试测试测试", None),
         None,
         ("测试测试测试4", None),
         ("测试测试测试5", None),
         ("测试测试测试6", None),
         ],
        True
        )
    droplist.set_size_request(-1, 100)
    
    navigatebar = Navigatebar(
        [(ui_theme.get_pixbuf("navigatebar/nav_recommend.png"), "导航1", None),
         (ui_theme.get_pixbuf("navigatebar/nav_repo.png"), "导航2", None),
         (ui_theme.get_pixbuf("navigatebar/nav_update.png"), "导航3", lambda : TabWindow("测试标签窗口", tab_window_items).show_all()),
         (ui_theme.get_pixbuf("navigatebar/nav_uninstall.png"), "导航4", None),
         (ui_theme.get_pixbuf("navigatebar/nav_download.png"), "导航5", None),
         (ui_theme.get_pixbuf("navigatebar/nav_repo.png"), "导航6", None),
         (ui_theme.get_pixbuf("navigatebar/nav_update.png"), "导航7", None),
         (ui_theme.get_pixbuf("navigatebar/nav_uninstall.png"), "导航8", None),
         ])
    application.main_box.pack_start(navigatebar, False)
    application.window.add_move_event(navigatebar)
    application.window.add_toggle_event(navigatebar)
    
    notebook_box = gtk.VBox()
    tab_1_box = gtk.VBox()
    tab_2_box = gtk.VBox()
    tab_4_box = gtk.VBox()
    tab_5_box = gtk.VBox()
    
    notebook = Notebook(
        [(ui_theme.get_pixbuf("music.png"), "分类列表", lambda : switch_tab(notebook_box, tab_1_box)),
         (ui_theme.get_pixbuf("web.png"), "网络浏览器", lambda : switch_tab(notebook_box, tab_2_box)),
         (ui_theme.get_pixbuf("music.png"), "专辑封面", lambda : switch_tab(notebook_box, tab_4_box)),
         (ui_theme.get_pixbuf("music.png"), "自定义控件", lambda : switch_tab(notebook_box, tab_5_box)),
         ])
    notebook_frame = HorizontalFrame(20)
    notebook_frame.add(notebook)
    application.main_box.pack_start(notebook_frame, False, False)
    
    application.main_box.pack_start(notebook_box, True, True)
    
    notebook_box.add(tab_1_box)
    
    # Add body box.
    body_box = gtk.HBox()
    horizontal_frame = HorizontalFrame()
    horizontal_frame.add(body_box)
    tab_1_box.pack_start(horizontal_frame, True, True)
    
    # Add scalebar.
    scalebar = HScalebar()
    scalebar_frame = HorizontalFrame()
    scalebar_frame.add(scalebar)
    tab_1_box.pack_start(scalebar_frame, False, False)
    
    vscalebar = VScalebar()
    vscale_box = gtk.HBox()
    vscale_box.pack_start(vscalebar, False, False)
    body_box.pack_start(vscale_box, False, False)
    
    # Add categorybar.
    # Note if you add list in categorybar make sure height is multiples of list length.
    # Otherwise last one item will heighter than Otherwise items.
    category_box = HPaned()
    body_box.add(category_box)
    categorybar = Categorybar([
            (app_theme.get_pixbuf("categorybar/word.png"), "测试分类", lambda : Tooltip("测试分类", 600, 400)),
            (app_theme.get_pixbuf("categorybar/win.png"), "测试分类", None),
            (app_theme.get_pixbuf("categorybar/web.png"), "测试分类", None),
            (app_theme.get_pixbuf("categorybar/professional.png"), "测试分类", None),
            (app_theme.get_pixbuf("categorybar/other.png"), "测试分类", None),
            (app_theme.get_pixbuf("categorybar/multimedia.png"), "测试分类", None),
            (app_theme.get_pixbuf("categorybar/graphics.png"), "测试分类", None),
            (app_theme.get_pixbuf("categorybar/game.png"), "测试分类", None),
            (app_theme.get_pixbuf("categorybar/driver.png"), "测试分类", None),
            ])
    category_box.add1(categorybar)
    
    # Add scrolled window.
    scrolled_window = ScrolledWindow()
    category_box.add2(scrolled_window)
    
    items_length = 1000

    items = map(lambda index: ListItem(
            "豆浆油条 测试标题 %04d" % index,
            "林俊杰 %04d" % index,
            "10:%02d" % index,
            ), range(0, items_length))
    
    list_view = ListView(
        [(lambda item: item.title, cmp),
         (lambda item: item.artist, cmp),
         (lambda item: item.length, cmp)])
    list_view.set_expand_column(0)
    list_view.add_titles(["歌名", "歌手", "时间"])
    list_view.add_items(items)
    list_view.connect("double-click-item", lambda listview, item, i, x, y: list_view.set_highlight(item))
    
    # list_view.connect("button-press-item", print_button_press)
    # list_view.connect("double-click-item", print_double_click)
    # list_view.connect("single-click-item", print_single_click)
    # list_view.connect("motion-notify-item", print_motion_notify)
        
    scrolled_window.add_child(list_view)
    
    # Add volume button.
    volume_button = VolumeButton(100, 0, 100, 2)
    volume_frame = HorizontalFrame(10, 0, 0, 0, 0)
    volume_frame.add(volume_button)
    tab_1_box.pack_start(volume_frame, False, False)
    
    # Add entry widget.
    entry_button = ImageButton(
        app_theme.get_pixbuf("entry/search_normal.png"),
        app_theme.get_pixbuf("entry/search_hover.png"),
        app_theme.get_pixbuf("entry/search_press.png"),
        )
    entry = TextEntry()
    entry.connect("action-active", print_entry_action)
    entry.set_size(150, 24)
    entry_label = Label("标签测试， 内容非常长")
    entry_label.set_text("标签的内容灰长灰长的长")
    entry_label.set_size_request(100, 30)
    entry_box = gtk.HBox(spacing=10)
    entry_box.pack_start(entry_label, False, False)
    entry_box.pack_start(entry, True, True)
    
    shortcust_entry = ShortcutKeyEntry("Ctrl + Alt + Q")
    shortcust_entry.set_size(150, 24)
    entry_box.pack_start(shortcust_entry, False, False)
    
    color_button = ColorButton()
    entry_box.pack_start(color_button, False, False)
    
    # Group 
    image_button_items = [
        (app_theme.get_pixbuf("toolbar/%s_normal.png" % name),
         app_theme.get_pixbuf("toolbar/%s_hover.png" % name),
         app_theme.get_pixbuf("toolbar/%s_press.png" % name),
         None) for name in ["search", "list", "add", "sort", "delete"]
        ]
        
    toggle_button_items = [
        (app_theme.get_pixbuf("control/%s_normal.png" % name),
         app_theme.get_pixbuf("control/%s_press.png" % name),
         None, None, None) for name in ["lyrics", "media", "playlist", "musicbox"]
        ]
    
    toggle_button_align = gtk.Alignment()
    toggle_button_align.set(0.5, 0.5, 0, 0)
    toggle_button_align.add(ToggleButtonGroup(toggle_button_items))
    entry_box.pack_start(ImageButtonGroup(image_button_items))
    entry_box.pack_start(toggle_button_align)
    
    # combobox
    combo_box = ComboBox(
        [("测试测试测试1", 1),
         ("测试测试测试2", 2),
         ("测试测试测试3", 3),
         None,
         ("测试测试测试", 4),
         None,
         ("测试测试测试4", 5),
         ("测试测试测试5", 6),
         ("测试测试测试6", 7),
         ],
        100
        )
    entry_box.pack_start(combo_box, False, False)    
    entry_box.pack_start(SpinBox(3000, 0, 5000, 100), False, False)
    
    entry_frame = HorizontalFrame(10, 0, 0, 0, 0)
    entry_frame.add(entry_box)
    tab_1_box.pack_start(entry_frame, False, False)
    
    # Add statusbar.
    statusbar = Statusbar(36)
    tab_1_box.pack_start(statusbar, False)
    application.window.add_move_event(statusbar)
    application.window.add_toggle_event(statusbar)
    
    web_view = WebView()
    web_scrolled_window = ScrolledWindow()
    web_scrolled_window.add(web_view)
    web_view.open("http://www.linuxdeepin.com")
    tab_2_box.pack_start(web_scrolled_window)
    
    icon_view_hframe = HorizontalFrame()
    icon_view_vframe = gtk.Alignment()
    icon_view_vframe.set(0, 0, 1, 1)
    icon_view_vframe.set_padding(0, 1, 0, 0)
    
    icon_view_scrolled_window = ScrolledWindow()
    icon_view = IconView(10, 10)
    # icon_view = IconView()
    icon_view_scrolled_window.add_child(icon_view)
    icon_view_hframe.add(icon_view_scrolled_window)
    
    icon_view_vframe.add(icon_view_hframe)
    
    icon_items = map(lambda index: IconItem(
            app_theme.get_pixbuf("cover/%s.jpg" % (index)).get_pixbuf()
            ), range(1, 33))
    icon_view.add_items(icon_items)
    
    tab_4_box.pack_start(icon_view_vframe, True, True)
    
    # Tab 5.
    button_box = gtk.VBox()
    check_button = CheckButton("Check Button")
    radio_button_1 = RadioButton("Radio Button1")
    radio_button_2 = RadioButton("Radio Button2")
    button_box.pack_start(check_button, False, False, 4)
    button_box.pack_start(radio_button_1, False, False, 4)
    button_box.pack_start(radio_button_2, False, False, 4)
    tab_5_box.pack_start(button_box, False, False)
    
    # Tree view.
    def tree_view_single_click_cb(widget, item):
        pass    

    
    tree_view = TreeView()
    tree_view_scrolled_window = ScrolledWindow()
    tree_view_scrolled_window.add_child(tree_view)
    tree_view.connect("single-click-item", tree_view_single_click_cb)    
    
    tab_5_box.pack_start(tree_view_scrolled_window)
    
    wuhan_node = tree_view.add_item(None, TreeViewItem("Linux Deepin"))

    wuhan_dev_node = tree_view.add_item(wuhan_node, TreeViewItem("test1"))
    wuhan_des_node = tree_view.add_item(wuhan_node, TreeViewItem("test2"))
    wuhan_sys_node = tree_view.add_item(wuhan_node, TreeViewItem("test3"))
    
    tree_view.add_item(wuhan_dev_node, TreeViewItem("Deepin Music Player"))    
    tree_view.add_item(wuhan_dev_node, TreeViewItem("Deepin Media Player"))
    tree_view.add_item(wuhan_dev_node, TreeViewItem("Deepin Software Center"))
    
    tree_view.add_item(wuhan_sys_node, TreeViewItem("Deepin Talk"))    
    tree_view.add_item(wuhan_sys_node, TreeViewItem("Deepin IM"))
    tree_view.add_item(wuhan_sys_node, TreeViewItem("Deepin Reader"))
    
    tree_view.add_item(wuhan_des_node, TreeViewItem("ZHL"))    
    tree_view.add_item(wuhan_des_node, TreeViewItem("ZHL"))
    tree_view.add_item(wuhan_des_node, TreeViewItem("zhm"))
    
    beijing_node = tree_view.add_item(None, TreeViewItem("深度 Linux"))    
    tree_view.add_items(beijing_node, [TreeViewItem(name) for name in ("开发部", "设计部", "系统部")])
    
    text_view = TextView("this is line one\nline break is awesome\nblahblahlooooooooooooooooooooooooooooooooooooooooooooooooooooooooog")
    sw = ScrolledWindow()
    text_viewport = gtk.Viewport()
    text_viewport.add(text_view)
    sw.add(text_viewport)
    tab_5_box.pack_start(sw, True, True)
    
    # Run.
    application.run()
