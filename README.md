# DGutils

DGutils is a python module with some universal classes and methods to provide shortcuts
for some GTK operations, like Gio actions or managing bindings and connections to better
control objects' lifetime.

## DGutils contents

### `dgutils.Actions`
A class that loads actions from a YAML file from GResource and add
them to a class by a single decorator `@Actions.from_schema(...)`. This removes monstrous
code block of adding every action group from the class definiton

### `dgutils.Linker`
A class that should be used as a parent of the GObject class. Used for managing GObject's
bindings and connections, which may be usefull when using widget factories, like in
Gtk.ListView or GridView, when you always need to bind and unbind some properties and
connect/disconnect some callbacks of reused widgets.

### `dgutils.Schema`
A _dotted-path_ settings schema that stores all its values on key
chains like `root.state.window.width`. This schema support GOBject binding to re-implement
the GSchema behavior, which I found inconvinient. Its `bind()` method also support
value transforming between an object and schema. Default schema is defined in YAML file
and user schema is stored in JSON file

### `dgutils.singleton`
A module with `Singleton` and `GSingleton` metaclasses, which should
be used if you want to create a singleton object. `Singleton` is used for non-GObject
classes and `GSingleton` is used for GOBject classes

### `dgutils.decorators`
A module with some usefull decorators, like `final`, `baseclass`,
`singleton` and `errsingleton`