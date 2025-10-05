from js import console

from puepy import Application, Page, t

from iching import Oracle, PATTERNS

app = Application()


@app.page()
class IChingPage(Page):
    def initial(self):
        return {"question": ""}

    def populate(self):
        t.h1("Hello from I-Ching!")
        with t.div(class_name="iching-widget"):
            t.h3("Your I-Ching Fortune", )
            t.textarea(rows=3, bind="question", ref="iching_question")
            t.wa_button(
                "Ask the Oracle",
		on_click=self.tell_fortune
            )

    def tell_fortune(self, event):
        oracle = Oracle(question=self.state['question'])
        oracle.hexagram.generate()
        fortune = PATTERNS[oracle.hexagram.pattern]
        with t.div():
            t.h3(f"You asked: {self.state['question']}")
            t.h3(f"I-Ching responded: {fortune['character']}")
            t.p(fortune['name'])
           

 

app.mount("#app")
