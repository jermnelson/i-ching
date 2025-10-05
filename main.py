import datetime

from js import console

from puepy import Application, Page, t
from puepy.core import html

from iching import Oracle, PATTERNS

app = Application()


@app.page()
class IChingPage(Page):
    def initial(self):
        return {"question": "", "history": []}


    def fortune(self, fortune: dict):
        with t.wa_card(class_name="fortune"):
            t.h4(fortune['created'].isoformat())
            t.h3(f"You asked the I-Ching {fortune['question']}", slot="header")
            with t.dl():
               t.dt(html(fortune['character']), class_name="hexagram")
               t.dd(fortune['name'])

    def populate(self):
        t.h1("Hello from I-Ching!")
        with t.div(class_name="iching-widget"):
            t.h3("Your I-Ching Fortune", )
            t.textarea(rows=3, bind="question", ref="iching_question")
            t.wa_button(
                "Ask the Oracle",
		on_click=self.tell_fortune
            )
        with t.div(class_name="fortune-history"):
            t.h3("Fortune History")
            with t.ul():
                for fortune in self.state.get('history',[]):
                    with t.li():
                        self.fortune(fortune) 
                
    def tell_fortune(self, event):
        oracle = Oracle(question=self.state['question'])
        oracle.hexagram.generate()
        fortune = PATTERNS[oracle.hexagram.pattern]
        fortune["created"] = datetime.datetime.now(datetime.UTC)
        fortune["question"] = self.state["question"]
        console.log(f"Fortune {fortune} {self.state}")
        with self.state.mutate("history"):
            self.state["history"].append(fortune)
        with self.state.mutate("question"):
            self.state["question"] = ""

            
           

 

app.mount("#app")
