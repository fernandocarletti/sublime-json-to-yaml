import sublime
import sublime_plugin
import yaml
import json
import sys

jsonSyntaxFile = "Packages/YAML/YAML.sublime-syntax"
yamlSyntaxFile = "Packages/JavaScript/JSON.sublime-syntax"


class JsonToYamlCommand(sublime_plugin.TextCommand):
    def load_json(self, text):
        try:
            data = json.loads(text)
            return (True, data)
        except ValueError:
            return (False, {})

    def load_yaml(self, text):
        try:
            data = yaml.safe_load(text)
            return (True, data)
        except yaml.error.YAMLError:
            return (False, {})

    def run(self, edit):
        failed_regions = []

        selections = self.view.sel()

        # for selection in selections:
        #     print(selection.begin(), selection.end())

        regions = []
        for selection in selections:
            begin = selection.begin()
            end = selection.end()

            if len(selections) == 1 and selection.begin() == selection.end():
                begin = 0
                end = self.view.size()

            region = sublime.Region(begin, end)
            text = self.view.substr(region)

            result = self.load_json(text)
            dataFormat = "json"

            if not result[0]:
                result = self.load_yaml(text)
                dataFormat = "yaml"

            if not result[0]:
                failed_regions.append(region)
                continue

            data = result[1]

            if dataFormat == "json":
                self.view.replace(edit, region, yaml.dump(data).strip())
                self.view.set_syntax_file(yamlSyntaxFile)
            else:
                self.view.replace(edit, region, json.dumps(data, indent=2).strip())
                self.view.set_syntax_file(jsonSyntaxFile)

        if len(failed_regions) > 0:
            regions = ", ".join(map(lambda r: str(r.begin()), failed_regions))
            sublime.status_message("Conversion error: invalid data format")
