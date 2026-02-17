from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Static
from textual import events

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
        self.buttons = [self.query_one(f"#btn{i}", Button) for i in [7,8,9]] + [self.query_one("#div", Button)] + \
                       [self.query_one(f"#btn{i}", Button) for i in [4,5,6]] + [self.query_one("#mul", Button)] + \
                       [self.query_one(f"#btn{i}", Button) for i in [1,2,3]] + [self.query_one("#sub", Button)] + \
                       [self.query_one("#clear", Button), self.query_one("#btn0", Button), 
                        self.query_one("#eq", Button), self.query_one("#add", Button)]
        self.current_focus = 0
        self.buttons[0].focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        key_map = {"btn0": "0", "btn1": "1", "btn2": "2", "btn3": "3", "btn4": "4",
                   "btn5": "5", "btn6": "6", "btn7": "7", "btn8": "8", "btn9": "9",
                   "add": "+", "sub": "-", "mul": "*", "div": "/", "eq": "=", "clear": "C"}
        self.handle_input(key_map[event.button.id])

    def on_key(self, event: events.Key) -> None:
        if event.key == "space":
            self.buttons[self.current_focus].press()
            return
        
        key_map = {"0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", 
                   "6": "6", "7": "7", "8": "8", "9": "9", "plus": "+", "minus": "-",
                   "asterisk": "*", "slash": "/", "equals": "=", "enter": "=", "c": "C",
                   "h": "left", "j": "down", "k": "up", "l": "right",
                   "left": "left", "right": "right", "up": "up", "down": "down",
                   "backspace": "backspace"}
        if event.key in key_map:
            action = key_map[event.key]
            if action == "left":
                self.current_focus = (self.current_focus - 1) % len(self.buttons)
                self.buttons[self.current_focus].focus()
            elif action == "right":
                self.current_focus = (self.current_focus + 1) % len(self.buttons)
                self.buttons[self.current_focus].focus()
            elif action == "up":
                self.current_focus = (self.current_focus - 4) % len(self.buttons)
                self.buttons[self.current_focus].focus()
            elif action == "down":
                self.current_focus = (self.current_focus + 4) % len(self.buttons)
                self.buttons[self.current_focus].focus()
            else:
                self.handle_input(action)

    def handle_input(self, key: str) -> None:
        display = self.query_one("#display", Static)
        
        if key == "C":
            self.expression = ""
            display.update("0")
        elif key == "backspace":
            self.expression = self.expression[:-1]
            display.update(self.expression or "0")
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
