import json
from functools import wraps

import yaml
from gi.repository import Gio, Gtk


class Actions:
    """Creates `Gio.SimpleAction`s from provided GResource schema file.

    Could be used as a subclass and then call `super().__init__()` or by using `cls.from_schema()` class decorator
    """

    def __init__(self, instance, schema: dict):
        self.instance = instance
        self.schema = schema
        self._setup()

    def _setup(self):
        for group_name, actions in self.schema.get("groups", {}).items():
            action_group = Gio.SimpleActionGroup.new()
            shortcut_controller = Gtk.ShortcutController()

            for action in actions:
                name = action["name"]
                callback_name = action["callback"]
                callback = self._resolve_callback(callback_name)

                gio_action = Gio.SimpleAction.new(name, None)
                args = action.get("with_args", [])

                if args:
                    gio_action.connect("activate", lambda act, p: callback(*args))
                else:
                    gio_action.connect("activate", callback)

                action_group.add_action(gio_action)

                if shortcut := action.get("shortcut"):
                    shortcut_controller.add_shortcut(
                        Gtk.Shortcut.new(
                            trigger=Gtk.ShortcutTrigger.parse_string(shortcut),
                            action=Gtk.NamedAction.new(f"{group_name}.{name}"),
                        )
                    )

            self.instance.insert_action_group(group_name, action_group)
            self.instance.add_controller(shortcut_controller)

    def _resolve_callback(self, name: str):
        parts = name.split(".")
        obj = self.instance
        for part in parts:
            obj = getattr(obj, part)
        return obj

    @classmethod
    def from_schema(cls, path: str, encoding: str = "yaml"):
        """Creates actions from provided schema and adds them to a decorated class"""

        def class_decorator(target_cls):
            original_init = target_cls.__init__

            @wraps(original_init)
            def new_init(self, *args, **kwargs):
                original_init(self, *args, **kwargs)

                gfile = Gio.File.new_for_uri(f"resource://{path}")
                contents = gfile.load_contents(None)[1]
                decoded = contents.decode("utf-8")
                schema = (
                    yaml.safe_load(decoded)
                    if encoding == "yaml"
                    else json.loads(decoded)
                )

                cls(self, schema)

            target_cls.__init__ = new_init
            return target_cls

        return class_decorator
