==========
TkAutoBox
==========

Abstract
========

Tkinter provides several convenience functions for common dialogs like file dialogs or color dialogs.  I wanted a similar convenience function for arbitrary dialogs that could ask an easily-extendible set of fields and simply return a dict of values when clicked.  This can be useful for things like login dialogs, simple configuration dialogs, or installation/setup dialogs.

The TkAutoBox module is a python3 module that implements a generic convience function for this, as well as wrapper functions for common dialogs.

Usage
=====

Basic usage is pretty simple::

    from tkautobox import *

    values = autobox(fields = [
        {"name" : "foo"},
	{"name" : "bar", "type" : "checkbox", "label" : "Bar?"}
        ])
    print(values)

The "fields" list should contain dicts defining each field you want on the dialog form.  The field dicts need, at minimum, a "name" item, which will be the key used for that value in the dict that is returned.  The name will also be used to label the field, unless "label" is provided.

There's also a loginbox() function to provide a typical login box with username and password fields::

    from tkautobox import *
    credentials = loginbox()
    print(credentials)

You can extend this login box with additional fields easily with the "additional_fields" keyword argument.

Reference
=========

Autobox
-------

This is the class that implements the autobox.  You don't probably want to instantiate this directly, but rather use the convenience functions.

autobox()
---------

This is the wrapper function for the generic dialog box.  When called, it will create and show the dialog; when the user clicks the OK button, the dialog will close and the function returns a dict of name/value pairs for the form.  It takes no positional arguments, but the following keyword arguments are accepted:

:title_string: The string to display in the title bar of the dialog
:header_string: A string to dislplay at the top of the dialog
:error_message: A message to display in red text below the header string
:ok_label: The string to put on the OK button.  Default is "OK".
:theme: A TK theme to use for the dialog
:padding: The padding, in pixels, to use around the widgets.  Default is 5.
:fields: A list of dicts specifying the fields to put on the page.

Each dict in the fields list can take the following keys:

:name: A name for the field.  The returned dict will use this as a key.
:label: A label to use on the form for this field, if you want it to be different from the name.
:type: The type of widget to use, can be:

        - "text" (regular text entry)
	- "hidden_text" (obfuscated text entry, e.g. password fields),
        - "checkbox" (takes a Boolean)
	- "select" (drop-down select box)

:default: The default value to set this field to.  Must be a valid type and value for the widget.
:options: For "select" type fields, a list of strings to provide as options.  For other types, this value is ignored.

The "name" field is the only one required.  "type" defaults to "text" if omitted, and "label" defaults to using the "name" value if omitted.


loginbox()
----------

The loginbox() function is a wrapper around autobox() that provides a standard login dialog with "username" and "password" fields.  It can accept all the same keyword arguments as autobox(), but should not define the "fields" list.  It accepts the following extra keywords:

:additional_fields: A list, using identical syntax to autobox's "fields" list, that will define additonal fields below "password" (e.g., domain, database, etc.).
:default_username: A username to populate the "username" field with.


Contributing
============

Please report bugs, and feel free to submit patches for code or documentation.

License
=======

TkAutoBox is distributed under the terms of the Simplified BSD license.  See the attached COPYING file for details.
