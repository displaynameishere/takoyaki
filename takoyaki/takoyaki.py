from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Label

class Takoyaki(App):
    CSS_PATH = "takoyaki.tcss"
    TITLE = "takoyaki"

    def on_mount(self) -> None:
        self.screen.styles.background = "black"

    def compose(self) -> ComposeResult:
        yield Header(id="header")


if __name__ == "__main__":
    app = Takoyaki()
    app.run()