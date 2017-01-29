import os
import json

import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import Menu
from tkinter import PhotoImage
from tkinter import messagebox
import tkinter.scrolledtext as tkst
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

from RJSorts import RJSorts
from CaseLog import CaseLog
from ReadWriteExcel import ReadWriteExcel
from CreateFaceSheets import CreateFaceSheets

MESSAGE1 = ('Before continuing you must select a case log.\n\n'
            'If a case log does not exist I will help you create one.\n\n'
            'Click the "Case Log" menu above and select or create a case log.\n\n')

MESSAGE2 = 'Please select the Restorative Justice Excel file generated from LERMs.\n\n'

MESSAGE3 = 'You have selected {} as the report generated from LERMs.\n\n'

MESSAGE4 = 'You have created your Case Log.\n\nPlease select the Restorative Justice Excel file generated from LERMs.\n\n'

MESSAGE5 = 'You have selected {} as your case log.\n\n'

MESSAGE6 = 'Checking the Case Log.\n\n'

MESSAGE7 = 'Sorting the excel file.\n\n'

MESSAGE8 = 'Select the incident types to be considered.\n\n'


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


class MenuBar(tk.Menu):

    def __init__(self, controller):
        tk.Menu.__init__(self, controller)
        self.controller = controller

        ############################## Sub-Menu ##############################

        fileMenu = tk.Menu(self, activeborderwidth=1, tearoff=False)
        self.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='Exit', command=self.quit)

        ############################## Sub-Menu ##############################

        caselog = tk.Menu(self, activeborderwidth=1, tearoff=False)
        self.add_cascade(label='Case Log', menu=caselog)
        caselog.add_command(label='Select Log', command=self.select_log_path)
        caselog.add_separator()
        caselog.add_command(label='Create Log', command=self.create_new_log)

        ############################## Sub-Menu ##############################

        defaults = tk.Menu(self, activeborderwidth=1, tearoff=False)
        self.add_cascade(label='Defaults', menu=defaults)
        defaults.add_command(label='Display current defaults', command=self.display_defualts)
        defaults.add_separator()
        defaults.add_command(label='Make current selections default', command=self.change_defaults)
        defaults.add_separator()
        defaults.add_command(label='Restore deaults', command=self.restore_defaults)


    ############################## Helper Functions ##########################

    def select_log_path(self):
        file_types = [('Excel file ending with .xlsx', '*.xlsx'), ]
        log_path = askopenfilename(filetypes=file_types, title='Select your Case Log')

        if log_path:
            self.controller.defaults['PATH'] =  log_path
            with open('app_files/defaults.json', 'w') as jsonFile:
                jsonFile.write(json.dumps(self.controller.defaults))
                file_name = os.path.basename(self.controller.defaults['PATH'])
                self.controller.frames['OutputFrame'].update_output_text(MESSAGE5.format(file_name))
                self.controller.frames['ButtonFrame'].select_button.config(state='normal')

    def create_new_log(self):
        file_types = [('Excel file ending with .xlsx', '*.xlsx'), ]
        log_path = asksaveasfilename(filetypes=file_types, initialfile='Case_Log', title='Save the Case Log')
        
        if log_path:
            self.controller.defaults['PATH'] = log_path
            with open('app_files/defaults.json', 'w') as jsonFile:
                jsonFile.write(json.dumps(self.controller.defaults))
                log = ReadWriteExcel(self.controller.defaults['PATH'])
                log.create_worksheets(['Case Log'])
                log.save_workbook()
                self.controller.frames['OutputFrame'].update_output_text(MESSAGE4)
                self.controller.frames['ButtonFrame'].select_button.config(state='normal')

    def display_defualts(self):
        self.controller.frames['OutputFrame'].update_output_text('-' * 80 + '\n')
        for default in self.controller.defaults['DEFAULT_LIST']:
            self.controller.frames['OutputFrame'].update_output_text(default + '\n')
        self.controller.frames['OutputFrame'].update_output_text('-' * 80 + '\n\n')

    def change_defaults(self):
        self.controller.defaults['DEFAULT_LIST'] = self.controller.frames['SelectionFrame'].current_selection()
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

        self.select_button = ttk.Button(self, text='Select', command=self.get_path)
        self.run_button = ttk.Button(self, text='Run', command= lambda: self.controller.AppLogic.run())

        ############################### LAYOUT ###############################

        pad = 10
        self.run_button.pack(side='right', pady=pad, padx=pad)
        self.select_button.pack(side='right', pady=pad, padx=pad)
        self.run_button.config(state='disabled')
        self.select_button.config(state='disabled')

    ############################## Helper Functions ##########################

    def get_path(self):
        file_types = [('Excel file ending with .xlsx', '*.xlsx'), ]
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
                                  width=width, bg='#000000', foreground='#00ff00',
                                  selectbackground='#00ff00')

        self.listbox.config(yscrollcommand=scrollbar.set,)
        scrollbar.config(command=self.listbox.yview)

        ############################### LAYOUT ###############################

        scrollbar.pack(side='right', fill='y')
        self.listbox.pack(fill='both', expand='1')
        self.update_list([' Incident Types '])

    ############################## Helper Functions ##########################

    def update_list(self, selection_list):
        self.listbox.delete(0, 'end')
        selection_list = list(set(selection_list))
        selection_list.sort()
        for item in selection_list:
            self.listbox.insert('end', item)

        for default in self.controller.defaults['DEFAULT_LIST']:
            if default in selection_list:
                self.listbox.select_set(selection_list.index(default))

    def current_selection(self):
        selected = [self.listbox.get(item) for item in self.listbox.curselection()]
        return selected


class AppLogic(tk.Frame):

    def __init__(self, controller):
        self.log = None
        self.sorts = None
        self.controller = controller
        if os.path.isfile(self.controller.defaults['PATH']):
            self.controller.frames['ButtonFrame'].select_button.config(state='normal')
            self.controller.frames['OutputFrame'].update_output_text(MESSAGE2)
        else:
            self.controller.frames['OutputFrame'].update_output_text(MESSAGE1)

    def report_selected(self, path):
        file_name = os.path.basename(path)
        self.controller.frames['OutputFrame'].update_output_text(MESSAGE3.format(file_name))
        self.check_case_log(path)
        self.create_sorter(path)

    def check_case_log(self, LERMs_report_path):
        self.controller.frames['OutputFrame'].update_output_text(MESSAGE6)
        self.log = CaseLog(self.controller.defaults['PATH'])
        self.log.compare_previous_current(LERMs_report_path)
        self.log.save_log()

    def create_sorter(self, path):
        self.sorts = RJSorts(path, self.log.rows_to_check)
        selection_list = self.sorts.unsorted.copy_col(self.sorts.headers.index('case occurred incident type') + 1, self.log.lowest_row_index)
        self.controller.frames['SelectionFrame'].update_list(selection_list)
        self.controller.frames['ButtonFrame'].run_button.config(state='normal')
        self.controller.frames['OutputFrame'].update_output_text(MESSAGE8)

    def run(self):
        self.controller.frames['OutputFrame'].update_output_text(MESSAGE7)
        self.sorts.sort_dict['case occurred incident type'] = self.controller.frames['SelectionFrame'].current_selection()
        self.sorts.check_sheet()
        file_types = [('Excel file ending with .xlsx', '*.xlsx'), ]
        results_path = asksaveasfilename(filetypes=file_types, initialfile='results', title='Save the Results?')
        self.sorts.save_results(results_path)
        facesheets = CreateFaceSheets(results_path)
        self.controller.frames['OutputFrame'].update_output_text('All Done.')


if __name__ == '__main__':
    app = RestorativeJusticeApp()
    app.mainloop()
