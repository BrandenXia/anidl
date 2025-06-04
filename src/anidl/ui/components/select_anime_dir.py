from typing import cast
from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.validation import Validator, ValidationResult
from textual.widgets import Input, OptionList, Rule

from anidl.config import Config
from anidl.utils.path import directory_completion

from .popup import PopupMenu


class PathValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            p = Path(value).expanduser()
        except RuntimeError:
            return self.failure("Invalid path format")
        if not p.exists():
            return self.failure("Path does not exist")
        if not p.is_dir():
            return self.failure("Path is not a directory")

        return self.success()


class SelectAnimeDir(PopupMenu):
    BINDINGS = [
        Binding("tab", "switch_completion", "Switch Completion", show=False),
        Binding(
            "shift+tab",
            "switch_completion(True)",
            "Switch Completion Reverse",
            show=False,
        ),
        Binding("ctrl+n", "switch_completion", "Switch Completion", show=False),
        Binding(
            "shift+tab",
            "switch_completion(True)",
            "Switch Completion Reverse",
            show=False,
        ),
        Binding("alt+backspace", "delete_word", "Delete Word", show=False),
    ]

    def update_completion(self, value: str) -> None:
        completions = list(map(str, directory_completion(value)))

        rule_widget = self.query_one(Rule)
        completions_widget = self.query_one(OptionList)
        display = "none" if len(completions) == 0 else "block"
        rule_widget.styles.display = completions_widget.styles.display = display

        completions_widget.clear_options()
        completions_widget.add_options(completions)

    def on_input_changed(self, event: Input.Changed) -> None:
        self.update_completion(event.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # TODO: handle the submission
        assert event.validation_result is not None
        if not event.validation_result.is_valid:
            self.notify(
                event.validation_result.failure_descriptions[0],
                title="Validation Failed",
                severity="warning",
            )
        Config().anime_dir = event.value
        self.close()

    def action_switch_completion(self, rev: bool = False) -> None:
        options_widget = self.query_one(OptionList)
        if len(options_widget.options) > 0:
            # if completions available, go to next option
            if not rev:
                options_widget.action_cursor_down()
            else:
                options_widget.action_cursor_up()

            if (index := options_widget.highlighted) is not None:
                # if an option is highlighted,
                # update the input with the selected completion
                # but prevent the Input.Changed event
                input_widget = self.query_one(Input)
                with input_widget.prevent(Input.Changed):
                    completed_text = cast(
                        str, options_widget.get_option_at_index(index).prompt
                    )
                    input_widget.value = completed_text
                    input_widget.cursor_position = len(completed_text)
        else:
            # if not, try to update completions
            input_widget = self.query_one(Input)
            self.update_completion(input_widget.value)

    def action_delete_word(self) -> None:
        input_widget = self.query_one(Input)
        input_widget.action_delete_left_word()

    def compose(self) -> ComposeResult:
        self.border_title = "Select Anime Directory"
        yield Input(
            "~/",
            select_on_focus=False,
            validators=PathValidator(),
            validate_on=["submitted"],
        )
        yield Rule()

        completions_widget = OptionList(compact=True)
        completions_widget.can_focus = False
        yield completions_widget
