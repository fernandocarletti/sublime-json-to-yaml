# Sublime JSON To Yaml

A sublime package to convert JSON to Yaml and vice-versa.

I did this for my personal use since it is a regular need to convert Yaml to JSON while managing Kubernetes with Pulumi.

## Goal

Be able to convert Json to Yaml and Yaml to Json, respecting the selections.

## Not a Goal

Formatting JSON or Yaml. Some packages Pretty JSON already handles formatting really well, another package is not needed for that.

## Differences Between SerializedDataConverter

This extension aims to convert the data in place, in the same file. You should be able to convert a small portion of the file by selecting the part you want to convert.

## Usage

You can call it by using the shortcut `Ctrl + Alt + T` in all operating systems.

You can also look for the `JSON to Yaml` and `Yaml to JSON` commands in the command pallete (`Ctrl/Command + Shift + P`).
