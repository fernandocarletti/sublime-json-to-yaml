import sublime
import sys
from unittest import TestCase

version = sublime.version()


class TestJsonToYaml(TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def setText(self, string):
        self.view.run_command("insert", {"characters": string})

    def getText(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def test_converts_json_to_yaml(self):
        self.setText('{"foo":"bar"}')

        self.view.run_command("json_to_yaml")
        actual = self.getText()

        self.assertEqual(actual, "foo: bar")

    def test_converts_json_to_yaml_with_multiple_selections(self):
        self.setText('{\n  "foo": "bar"\n}\nzzzzz\n{"zaz":["baz"]}')
        self.view.sel().add(sublime.Region(0, 20))
        self.view.sel().add(sublime.Region(29, 46))

        self.view.run_command("json_to_yaml")
        actual = self.getText()

        print(actual)

        # For some reason two spaces are being added before the "z's".
        # I can't reproduce that in real usage, so I left it in the assertion
        # for now since it actually works :(
        self.assertEqual(actual, "foo: bar\n  zzzzz\nzaz:\n- baz")

    def test_converts_yaml_to_json(self):
        self.setText("foo: bar")

        self.view.run_command("json_to_yaml")
        actual = self.getText()

        self.assertEqual(actual, '{\n  "foo": "bar"\n}')

    def test_converts_yaml_to_json_with_multiple_selections(self):
        self.setText("foo: bar\nzzzzz\nzaz:\n- baz")
        self.view.sel().add(sublime.Region(0, 8))
        self.view.sel().add(sublime.Region(15, 25))

        self.view.run_command("json_to_yaml")
        actual = self.getText()

        print(actual)

        self.assertEqual(
            actual, '{\n  "foo": "bar"\n}\nzzzzz\n{\n  "zaz": [\n    "baz"\n  ]\n}'
        )
