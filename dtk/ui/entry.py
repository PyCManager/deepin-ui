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

import gtk
import cairo
from utils import *
from draw import *

class Entry(gtk.EventBox):
    '''Entry.'''
	
    def __init__(self, content="", 
                 text_color=ui_theme.get_color("entryText"),
                 text_select_color=ui_theme.get_color("entrySelectText"),
                 background_color=ui_theme.get_shadow_color("entryBackground"),
                 background_select_color=ui_theme.get_shadow_color("entrySelectBackground"),
                 font_size=DEFAULT_FONT_SIZE, 
                 padding_x=10, padding_y=5):
        '''Init entry.'''
        # Init.
        gtk.EventBox.__init__(self)
        self.set_visible_window(False)
        self.set_can_focus(True) # can focus to response key-press signal
        self.im = gtk.IMMulticontext()
        self.font_size = font_size
        self.content = content
        self.cursor_index = 0
        self.offset_x = 0
        self.text_color = text_color
        self.text_select_color = text_select_color
        self.background_color = background_color
        self.background_select_color = background_select_color
        self.padding_x = padding_x
        self.padding_y = padding_y
        
        # Connect signal.
        self.connect("realize", self.realize_entry)
        self.connect("key-press-event", self.key_press_entry)
        self.connect("expose-event", self.expose_entry)
        self.connect("button-press-event", self.button_press_entry)
        
        self.im.connect("commit", self.commit_entry)
        
    def set_text(self, text):
        '''Set text.'''
        self.content = text

        self.queue_draw()
        
    def get_text(self):
        '''Get text.'''
        return self.content
        
    def realize_entry(self, widget):
        '''Realize entry.'''
        # Init IMContext.
        self.im.set_client_window(widget.window)
        self.im.focus_in()
        
    def key_press_entry(self, widget, event):
        '''Callback for `key-press-event` signal.'''
        # Pass key to IMContext.
        self.im.filter_keypress(event)
        
        return False
    
    def expose_entry(self, widget, event):
        '''Callback for `expose-event` signal.'''
        # Init.
        cr = widget.window.cairo_create()
        rect = widget.allocation
        x, y, w, h = rect.x, rect.y, rect.width, rect.height

        # Draw background.
        draw_hlinear(cr, x, y, w, h,
                     self.background_color.get_color_info())
        
        # Draw text.
        self.draw_entry_text(cr, rect)
        
        # Draw cursor.
        self.draw_entry_cursor(cr, rect)
        
        # Propagate expose.
        propagate_expose(widget, event)
        
        return True
    
    def draw_entry_text(self, cr, rect):
        '''Draw entry text.'''
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        with cairo_state(cr):
            # Clip text area first.
            draw_x = x + self.padding_x
            draw_y = y + self.padding_y
            draw_width = w - self.padding_x * 2
            draw_height = h - self.padding_y * 2
            cr.rectangle(draw_x, draw_y, draw_width, draw_height)
            cr.clip()
            
            # Create pangocairo context.
            context = pangocairo.CairoContext(cr)
            
            # Set layout.
            layout = context.create_layout()
            layout.set_font_description(pango.FontDescription("%s %s" % (DEFAULT_FONT, self.font_size)))
            layout.set_text(self.content)
            
            # Get text size.
            (text_width, text_height) = layout.get_pixel_size()
            
            # Move text.
            cr.move_to(draw_x - self.offset_x, 
                       draw_y + (draw_height - text_height) / 2)
    
            # Draw text.
            cr.set_source_rgb(*color_hex_to_cairo(self.text_color.get_color()))
            context.update_layout(layout)
            context.show_layout(layout)
            
    def draw_entry_cursor(self, cr, rect):
        '''Draw entry cursor.'''
        # Init.
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        left_str = self.content[0:self.cursor_index]
        right_str = self.content[self.cursor_index::]
        (left_str_width, left_str_height) = get_content_size(left_str, self.font_size)
        
        # Draw cursor.
        cr.set_source_rgb(*color_hex_to_cairo(ui_theme.get_color("entryCursor").get_color()))
        cr.rectangle(x + self.padding_x + left_str_width - self.offset_x,
                     y + self.padding_y,
                     1, 
                     h - self.padding_y * 2)
        cr.fill()
    
    def button_press_entry(self, widget, event):
        '''Button press entry.'''
        self.grab_focus()
        
    def commit_entry(self, im, input_text):
        '''Entry commit.'''
        self.content = self.content[0:self.cursor_index] + input_text + self.content[self.cursor_index::]
        self.cursor_index += len(input_text)
        
        (text_width, text_height) = get_content_size(self.content, self.font_size)
        rect = self.get_allocation()
        if text_width <= rect.width - self.padding_x * 2:
            self.offset_x = 0
        elif self.cursor_index == len(self.content):
            self.offset_x = text_width - (rect.width - self.padding_x * 2)
        else:
            (old_text_width, old_text_height) = get_content_size(self.content[0:self.cursor_index - len(input_text)])
            (input_text_width, input_text_height) = get_content_size(input_text)
            if old_text_width - self.offset_x + input_text_width > rect.width - self.padding_x * 2:
                (new_text_width, new_text_height) = get_content_size(self.content[0:self.cursor_index])
                self.offset_x = new_text_width - (rect.width - self.padding_x * 2)
        
        self.queue_draw()
        
gobject.type_register(Entry)

if __name__ == "__main__":
    window = gtk.Window()
    window.set_colormap(gtk.gdk.Screen().get_rgba_colormap())
    window.set_decorated(False)
    window.add_events(gtk.gdk.ALL_EVENTS_MASK)        
    window.connect("destroy", lambda w: gtk.main_quit())
    window.set_size_request(300, -1)
    window.move(100, 100)
    
    entry = Entry("Enter to search")
    window.add(entry)

    window.show_all()
    
    gtk.main()
