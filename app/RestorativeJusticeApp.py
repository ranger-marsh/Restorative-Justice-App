#!/usr/bin/env python3

import os
import json
import sqlite3
from pathlib import Path

import tkinter as tk
import tkinter.scrolledtext as tkst

from tkinter import ttk
from tkinter import font
from tkinter import Menu
from tkinter import IntVar
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import Checkbutton
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import csv_handler
import database_handler
from FaceSheetTemplate import FaceSheetTemplate


class RestorativeJusticeApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        with open('app_files/defaults.json', 'r') as jsonFile:
            self.defaults = json.load(jsonFile)

        self.wm_title('Restorative Justice App -- Produced by Scott Frasier')
        img = PhotoImage(file='app_files/icon.gif')
        self.tk.call('wm', 'iconphoto', self._w, img)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = dict()
        self.frames['ButtonFrame'] = ButtonFrame(parent=container, controller=self)
        self.frames['OutputFrame'] = OutputFrame(parent=container, controller=self)
        self.frames['SelectionFrame'] = SelectionFrame(parent=container, controller=self)

        self.frames['ButtonFrame'].grid(row=1, column=0, sticky='nsew')
        self.frames['OutputFrame'].grid(row=0, column=0, sticky='nsew')
        self.frames['SelectionFrame'].grid(row=0, column=1, rowspan=3, sticky='nsew')

        self.frames['ButtonFrame'].config()
        self.frames['OutputFrame'].config()
        self.frames['SelectionFrame'].config()

        menubar = MenuBar(self)
        self.config(menu=menubar, pady=10, padx=10)
        self.AppLogic = AppLogic(controller=self)

        db_path = Path('app_files/app_db.sqlite3')
        if db_path.is_file():
            self.db = sqlite3.connect('app_files/app_db.sqlite3')
            self.cursor = self.db.cursor()

        else:
            if messagebox.askokcancel('Database not found', 'Would you like to create a database?'):
                self.db = sqlite3.connect('app_files/app_db.sqlite3')
                self.cursor = self.db.cursor()
                database_handler.create_table(self.cursor)
                self.db.commit()
            else:
                quit()


class MenuBar(tk.Menu):

    def __init__(self, controller):
        tk.Menu.__init__(self, controller)
        self.controller = controller

        ############################## Sub-Menu ##############################

        file_menu = tk.Menu(self, activeborderwidth=1, tearoff=False)
        self.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Exit', command=self.quit)

        ############################## Sub-Menu ##############################

        defaults = tk.Menu(self, activeborderwidth=1, tearoff=False)
        self.add_cascade(label='Defaults', menu=defaults)
        defaults.add_command(label='Display current defaults', command=self.display_defualts)
        defaults.add_separator()
        defaults.add_command(label='Make current selections default', command=self.change_defaults)
        defaults.add_separator()
        defaults.add_command(label='Restore deaults', command=self.restore_defaults)

        ############################## Sub-Menu ##############################

        receipt_menu = tk.Menu(self, activeborderwidth=1, tearoff=False)
        self.add_cascade(label='Receipt', menu=receipt_menu)
        receipt_menu.add_command(label='Save receipt', command=self.save_receipt)

    ############################## Helper Functions ##########################

    def save_receipt(self):
        receipt_path = askdirectory(title='Save the Receipt?')
        rows = database_handler.receipt(self.controller.cursor)
        csv_handler.write_receipt(receipt_path, rows)

    def display_defualts(self):
        self.controller.frames[
            'OutputFrame'].update_output_text('-' * 80 + '\n')
        for default in self.controller.defaults['DEFAULT_LIST']:
            self.controller.frames['OutputFrame'].update_output_text(default + '\n')
        self.controller.frames['OutputFrame'].update_output_text('-' * 80 + '\n\n')

    def change_defaults(self):
        self.controller.defaults['DEFAULT_LIST'] = self.controller.frames[
            'SelectionFrame'].current_selection()
        with open('app_files/defaults.json', 'w') as jsonFile:
            jsonFile.write(json.dumps(self.controller.defaults))

    def restore_defaults(self):
        self.controller.defaults['DEFAULT_LIST'] = self.controller.defaults['RESTORE']
        with open('app_files/defaults.json', 'w') as jsonFile:
            jsonFile.write(json.dumps(self.controller.defaults))


class OutputFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ############################# UI Elements ############################

        self.output = tkst.ScrolledText(self, wrap='word', bg='#000000', foreground='#00ff00')

        ############################### LAYOUT ###############################

        self.output.pack(fill='both', expand='yes')
        self.update_output_text('Hello.\n\n')

    ############################## Helper Functions ##########################

    def update_output_text(self, message):
        self.output.config(state='normal')
        self.output.insert('insert', message)
        self.output.see('end')
        self.output.config(state='disabled')


class ButtonFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        ############################# UI Elements ############################

        self.select_button = ttk.Button(
            self, text='Select', command=self.get_path)
        self.run_button = ttk.Button(
            self, text='Run', command=lambda: self.controller.AppLogic.run())
        self.check_var1 = IntVar()
        self.check_var2 = IntVar()
        self.check_var1.set(1)
        self.check_var2.set(1)

        check_box1 = Checkbutton(self, text='Create Face-Sheets', variable=self.check_var1,
                                 onvalue=1, offvalue=0, height=5, width=15)
        check_box2 = Checkbutton(self, text='File by District', variable=self.check_var2,
                                 onvalue=1, offvalue=0, height=5, width=15)

        ############################### LAYOUT ###############################

        pad = 10
        self.run_button.pack(side='right', pady=pad, padx=pad)
        self.select_button.pack(side='right', pady=pad, padx=pad)
        self.run_button.config(state='disabled')

        check_box1.pack(side='left')
        check_box2.pack(side='left')

    ############################## Helper Functions ##########################

    def get_path(self):
        file_types = [('csv file ending with .csv', '*.csv'), ]
        lerms_report = askopenfilename(filetypes=file_types)
        if lerms_report:
            self.controller.AppLogic.report_selected(lerms_report)


class SelectionFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        mfont = font.Font(family='times', size=12)
        width = mfont.measure('')

        ############################# UI Elements ############################

        scrollbar = tk.Scrollbar(self, orient='vertical')
        self.listbox = tk.Listbox(self, yscrollcommand=scrollbar.set, selectmode='multiple',
                                  width=width, bg='#000000', foreground='#00ff00', selectbackground='#00ff00')

        self.listbox.config(yscrollcommand=scrollbar.set,)
        scrollbar.config(command=self.listbox.yview)

        ############################### LAYOUT ###############################

        scrollbar.pack(side='right', fill='y')
        self.listbox.pack(fill='both', expand='1')
        self.update_list([' Incident Types '])

    ############################## Helper Functions ##########################

    def update_list(self, selection_list):
        self.listbox.delete(0, 'end')
        selection_list = list(selection_list)
        selection_list.sort()
        for item in selection_list:
            self.listbox.insert('end', item)

        for default in self.controller.defaults['DEFAULT_LIST']:
            if default in selection_list:
                self.listbox.select_set(selection_list.index(default))

    def current_selection(self):
        selected = [self.listbox.get(item)
                    for item in self.listbox.curselection()]
        return selected


class AppLogic(tk.Frame):

    def __init__(self, controller):
        self.controller = controller
        self.controller.frames['OutputFrame'].update_output_text(
            'Please select the Restorative Justice Excel file generated from LERMs.\n\n')

    def report_selected(self, path):
        file_name = os.path.basename(path)
        self.controller.frames['OutputFrame'].update_output_text(
            f'You have selected {file_name} as the report generated from LERMs.\n\n')
        rows = csv_handler.open_csv(path)

        if rows:
            database_handler.insert_rows(self.controller.cursor, rows)
            self.controller.db.commit()
            selection_list = database_handler.offense_types(self.controller.cursor)

            self.controller.frames['SelectionFrame'].update_list(selection_list)
            self.controller.frames['ButtonFrame'].run_button.config(state='normal')

            self.controller.frames['OutputFrame'].update_output_text(
                'Select the incident types to be considered and press the Run button.\n\n')
        else:
            if not messagebox.askokcancel('Bad Headers!', 'Select a new csv file?'):
                quit()

    def run(self):
        offense_list = self.controller.frames['SelectionFrame'].current_selection()
        database_handler.fileter_data(self.controller.cursor, offense_list)
        self.controller.db.commit()

        create_face = self.controller.frames['ButtonFrame'].check_var1.get()
        file_by_district = self.controller.frames['ButtonFrame'].check_var2.get()

        if create_face:
            results_path = askdirectory(title='Save the Results?')

        for row in database_handler.query_status(self.controller.cursor, 0):
            database_handler.update_status(self.controller.cursor, 100, row[0])
            if create_face:
                facesheet = FaceSheetTemplate(row[17], row[1], row[7], row[15], row[14], row[12],
                                              row[5], row[8], row[9], row[10], row[11], row[13])
                facesheet.save_facesheet(results_path, file_by_district)
        self.controller.db.commit()

if __name__ == '__main__':
    app = RestorativeJusticeApp()
    app.mainloop()
    print('test quit')
