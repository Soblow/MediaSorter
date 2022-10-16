# TODO
## Vital
None

## Important
- Add main buttons settings to Option Dialog
- Weird file progression when empty list (videoSorter at least)

## Suggestions
- Similar to undo hide, allow putting back moved items to list
- Add docstrings to functions
- Volume info on UI (like a widget to graphically change it)
- For videos, keys/buttons to control position / skip sections
- Command line arguments (optional config as not positional, optional directory as positional)
- Multi-action binding
- Copy videos to clipboard
- Undo/Redo history list widget/dialog
- Popup with folder infos / file infos

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
- Display all images as a gallery
- Allow to select them
- Same onekey-oneaction mecanic

## Other
- Reverse search button?
- Dedup feature?
