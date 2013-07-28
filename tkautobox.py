#!/usr/bin/env python3
"""
TkAutoBox
by Alan D Moore, copyright 2013

Released under the Simplified BSD license.

This file implements a simple, generic data-entry dialog box convience wrapper in Tkinter.
It's useful for things like login boxes or small configuration dialogs.
It requires at least python 3.
The box is extensible with any number of custom fields simply by passing in a list of dicts.
"""

from tkinter import *
from tkinter.ttk import *
from tkinter import font


class Autobox(Tk):
    """
    This class should probably not be instantiated directly, but rather the various wrapper functions should be used.
    """
    variable_types = {"text": StringVar, "hidden_text": StringVar, "checkbox":BooleanVar, "select": StringVar}

    def __init__(self, **kwargs):
        """
        Valid keyword arguments:

        - title_string: String; will be the window title.
        - header_string: String; text shown at the top of the window.
        - fields: List;  These are the form fields to add.
          It should be a list of dictionaries, each with the format:
           {
            "name" : <name of field>, string (required),
            "label" : <label to display for field>, string, if not specified "name" will be used
            "type"  : <one of label, text, hidden_text, checkbox, or select>, string,
            "default" : <default value of widget>(depends on widget type),
            "options": <options for select; does nothing for others>list or tuple
           }
        - error_message: String; an error message to display
        - theme: String; The TK theme to use. invalid themes will be ignored.
        - padding: Integer; The number of pixels to put around elements.
        - ok_label: String; Text for the OK button, defaults to "OK"
        - cancel_label: String; Text for the Cancel button, defaults to "Cancel"
        """
        Tk.__init__(self)
        #Pull in the keyword arguments
        self.title_string = kwargs.get("title_string", "")
        self.header_string = kwargs.get("header_string", "")
        self.fields = kwargs.get("fields", [])
        self.padding = kwargs.get("padding",  5)
        self.error_message = kwargs.get("error_message", None)
        self.theme = kwargs.get("theme")
        self.ok_label = kwargs.get("ok_label", "OK")
        self.cancel_label = kwargs.get("cancel_label", "Cancel")
        #set theme, if it's valid
        s = Style()
        if self.theme in s.theme_names():
            s.theme_use(self.theme)

        # create fonts and styles
        headerfont = font.Font(size=14)
        errorfont = font.Font(size=12, weight='bold')
        s.configure('Error.TLabel', foreground='#880000', font=errorfont)

        #Create variables
        self.data = {}

        # Fields need, at minimum, a name, unless they're a label
        self.fields = [x for x in self.fields if x.get("name") or x.get("type") == "label"]

        # Create the dictionary of variables for the form
        for field in self.fields:
            fn = field.get("name")
            if field.get("type") != "label":
                self.data[fn] = self.variable_types[field.get("type", "text")]()
                self.data[fn].set(field.get("default", ""))

        #Build the UI
        self.title(self.title_string)
        self.widgets = {}
        if self.header_string:
            Label(text=self.header_string, font=headerfont).grid(row=0, column=0, columnspan=2, padx=self.padding, pady=self.padding)
        if self.error_message:
            Label(text=self.error_message, style='Error.TLabel').grid(row=1, column=0, columnspan=2, padx=self.padding, pady=self.padding)
        for n, field in enumerate(self.fields):
            fn = field.get("name")
            ft = field.get("type", "text")
            label = field.get("label", fn)
            rownum = n + 2
            label_column_span = 1
            
            if ft == "select":
                self.widgets[fn] = Combobox(textvariable = self.data[fn], values = field.get("options"), state="readonly")
            elif ft == "checkbox":
                self.widgets[fn] = Checkbutton(variable=self.data[fn])
            elif ft == "hidden_text":
                self.widgets[fn] = Entry(textvariable = self.data[fn], show="*")
            elif ft == "label":
                label_column_span = 2
            else:
                self.widgets[fn] = Entry(textvariable = self.data[fn])
            Label(text=label).grid(row=rownum, column=0, columnspan=label_column_span, padx=self.padding, pady=self.padding, sticky=W)
            self.widgets.get(fn) and self.widgets[fn].grid(row=rownum, column=1, padx=self.padding, pady=self.padding, sticky=W)

        #Add a spacer
        Label().grid(row=998, column=0, columnspan=2, pady=20)
        #Login/cancel buttons
        self.ok_button = Button(self, text=self.ok_label, command=self.ok_clicked)
        self.ok_button.grid(row=999, column=0)
        self.cancel_button = Button(self, text=self.cancel_label, command=self.cancel_clicked)
        self.cancel_button.grid(row=999, column=1)

        #Bind keystrokes
        self.bind("<Return>", self.ok_clicked)
        self.bind("<Escape>", self.cancel_clicked)

    def ok_clicked(self, *args):
        self.data = { key : var.get() for key, var in self.data.items() }
        self.data["_clicked_ok"] = True
        self.quit()

    def cancel_clicked(self, *args):
        self.data = {}
        self.quit()

def autobox(**kwargs):
    ab = Autobox(**kwargs)
    ab.mainloop()
    data = ab.data
    ab.destroy()
    return data

def loginbox(**kwargs):
    """
    This wrapper creates a simple login box with username and password.
    Additional field specifications can be added with the additional_fields keyword.
    The remaining keywords are passed on to the class.
    """
    
    additional_fields = kwargs.get("additional_fields") and kwargs.pop("additional_fields") or []
    ok_label = kwargs.get("ok_label", "Log In")
    default_username = kwargs.get("default_username") and kwargs.pop("default_username") or ""
    title = kwargs.get("title_string") and kwargs.pop("title_string") or "Log In"

    default_fields = [
        {"name":"username", "type": "text", "default": default_username, "label": "Username: " },
        {"name":"password", "type": "hidden_text", "label":"Password: "}
        ]
    fields = default_fields + additional_fields

    return  autobox(fields=fields, ok_label=ok_label, title_string=title, **kwargs)

def passwordbox(**kwargs):
    """
    This wrapper is for making a dialog for changing your password.  
    It will return the old password, the new password, and a confirmation.
    The remaining keywords are passed on to the autobox class.
    """
    
    additional_fields = kwargs.get("additional_fields") and kwargs.pop("additional_fields") or []
    title = kwargs.get("title_string", "Change your password")
    header = kwargs.get("header_string") and kwargs.pop("header_string") or "Change your password"
    
    default_fields = [
        {"type" : "label", "label" : "First type your old password"},
        {"name" : "old_password", "type" : "hidden_text", "label" : "Old Password: "},
        {"type" : "label", "label": "Now enter your new password twice"},
        {"name" : "new_password", "type" : "hidden_text", "label" : "New Password: "},
        {"name" : "confirm_password", "type" : "hidden_text", "label" : "Confirm Password: "}
    ]
    fields = default_fields + additional_fields
    return autobox(fields = fields, title_string = title, header_string = header, **kwargs)

if __name__ == '__main__':
    """
    This is a test example of how to use this code.
    """
    test_user = "SomeUser"
    test_password = "Password"
    error_message = None
    # Log in to our mythical domains
    while True:
        res = loginbox(
            header_string="Log in to secure server", title_string="Login",
            default_username=test_user, error_message=error_message, theme='classic',
            additional_fields = [
                {"type" : "label", "label": "(The password is 'Password')"},
                {"name":"domain", "type":"select", "options":["Local", "US.gov", "RU.gov"], "default": "Local", "label" : "Login Domain: "},
                {"name" : "pwchange", "type":"checkbox", "default": False, "label" : "Prompt for password change?"}
                ]
                )
        if res == {}:
            print("Authentication cancelled.")
            exit()
        elif res.get("username") == test_user and res.get("password") == test_password:
            break
        else:
            error_message = "Authentication failed"
    print("Authentication success!")

    # If selected, change the password for the chosen domain
    if (res.get("pwchange")):
        error_message = ""
        while True:
            pw_res = passwordbox(header_string = "Change password for {}".format(res.get("domain")), error_message=error_message)
            if pw_res.get("old_password") != "Password":
                error_message = "The old password is not correct!"
            elif pw_res.get("new_password") == "":
                error_message = "You cannot change to a blank password!"
            elif pw_res.get("new_password") != pw_res.get("confirm_password"):
                error_message = "The new passwords do not match; please try again"
            elif pw_res.get("new_password") == pw_res.get("old_password"):
                error_message = "The new password cannot be the same as the old password"
            else:
                error_message = ""
                break
        print(pw_res)
    if (autobox(header_string = "This is a great library, eh?", ok_label = "Yep", cancel_label="Nope")):
        print("rock on!")
    else:
        print("Well, yeah, meh...")
