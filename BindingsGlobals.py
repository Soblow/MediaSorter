"""
BindingsGlobals

Module providing description of different bindings actions
"""
import enum


class BindingActionType(enum.Enum):
    """
    Type of actions possible
    """
    empty = 1  # Do nothing
    fileModification = 2  # Move/Copy/Delete/... the file
    listModification = 3  # Modify media list (remove from list)
    uiModification = 4  # Modify the UI (Zoom...)


# Possible action for bindings
bindingActions = {'nothing': [BindingActionType.empty], 'move': [BindingActionType.fileModification],
                  'copy': [BindingActionType.fileModification]}
