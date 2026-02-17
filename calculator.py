from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Static

class Calculator(App):
    CSS = """
    Screen { align: center middle; }
    Grid { grid-size: 4; width: 40; height: 20; }
    #display { column-span: 4; content-align: right middle; background: $panel; }
    Button { width: 100%; height: 100%; }
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            Static("0", id="display"),
            Button("7", id="btn7"), Button("8", id="btn8"), Button("9", id="btn9"), Button("/", id="div"),
            Button("4", id="btn4"), Button("5", id="btn5"), Button("6", id="btn6"), Button("*", id="mul"),
            Button("1", id="btn1"), Button("2", id="btn2"), Button("3", id="btn3"), Button("-", id="sub"),
            Button("C", id="clear"), Button("0", id="btn0"), Button("=", id="eq"), Button("+", id="add"),
        )

    def on_mount(self) -> None:
        self.expression = ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        display = self.query_one("#display", Static)
        btn_id = event.button.id
        
        key_map = {"btn0": "0", "btn1": "1", "btn2": "2", "btn3": "3", "btn4": "4",
                   "btn5": "5", "btn6": "6", "btn7": "7", "btn8": "8", "btn9": "9",
                   "add": "+", "sub": "-", "mul": "*", "div": "/", "eq": "=", "clear": "C"}
        key = key_map[btn_id]
        
        if key == "C":
            self.expression = ""
            display.update("0")
        elif key == "=":
            try:
                result = str(eval(self.expression))
                display.update(result)
                self.expression = result
            except:
                display.update("Error")
                self.expression = ""
        else:
            self.expression += key
            display.update(self.expression)

if __name__ == "__main__":
    Calculator().run()
