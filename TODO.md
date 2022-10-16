# TODO
## Vital
None

## Important
- Similar to undo hide, allow putting back moved items to list
- Current indexing method doesn't guarantee any order
  - An option to autosort once sorting is done
  - Option to select sorting method
  - A menu option to sort list
- Options menu (history size, main buttons...)
- Weird file progression when empty list (videoSorter at least)

## Suggestions
- Add docstrings to functions
- Option to recursively index folders?
- Volume info on UI (like a widget to graphicaly change it)
- For videos, keys to control position / skip sections
- Command line arguments (optional config as not positional, optional directory as positional)
- Multi-action binding
- Folder infos
- Copy/paste videos
- Undo/Redo history list widget
- Popup with folder infos / file infos
- Rotate images?

## Migration to Qt6
- Required for some new features
  - Listing available video formats at runtime instead of relying on a hardcoded list
    - https://doc.qt.io/qt-6/videooverview.html#determining-supported-media-formats-at-runtime
- Qt5 is deprecated
- Migration doesn't seem to break too many things
  - Check if supported on "all" OSes
  - PyQt6? PySide?

## Docker-based UI?
- Movable "containers" with config, status, view, infos...

## Gallery
- Display all images as a galery
- Allow to select them
- Same onekey-oneaction mecanic

## Other
- Reverse search button?
