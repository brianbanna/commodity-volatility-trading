"""Shared utilities: config loading, path resolution, manifest and checksum helpers.

Config is read only through the loader here. A science module never opens a yaml file
directly and never hardcodes a threshold, a cost, or a release timestamp.

The manifest and checksum helpers are the guard on the collection jobs: they detect a gap
or a silently changed upstream file. Treat an alarm from here as the highest priority
incident in this repo.
"""
