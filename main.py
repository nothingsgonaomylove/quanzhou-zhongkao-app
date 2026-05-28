
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp

DISTRICT_DATA = {
    "南安市": {
        "学校": [
            {"name": "南安一中", "min_score": 736.6},
            {"name": "国光中学", "min_score": 705.9},
            {"name": "侨光中学", "min_score": 689.0},
        ]
    },
    "惠安县": {
        "学校": [
            {"name": "惠安一中", "min_score": 733.8},
            {"name": "荷山中学", "min_score": 677.9},
        ]
    }
}

class Card(BoxLayout):
    def __init__(self, school, advice, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(10)
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(120)

        self.add_widget(Label(
            text=f"[b]{school['name']}[/b]",
            markup=True,
            font_size="20sp"
        ))

        self.add_widget(Label(
            text=f"2025录取线：{school['min_score']}",
            font_size="16sp"
        ))

        self.add_widget(Label(
            text=f"推荐等级：{advice}",
            font_size="16sp"
        ))

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = dp(10)
        self.spacing = dp(10)

        self.add_widget(Label(
            text="🏫 泉州中考志愿推荐系统",
            font_size="26sp",
            size_hint_y=None,
            height=dp(60)
        ))

        self.district = Spinner(
            text="南安市",
            values=list(DISTRICT_DATA.keys()),
            size_hint_y=None,
            height=dp(50)
        )
        self.add_widget(self.district)

        self.score_input = TextInput(
            hint_text="请输入分数",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(50)
        )
        self.add_widget(self.score_input)

        btn = Button(
            text="智能推荐",
            size_hint_y=None,
            height=dp(55)
        )
        btn.bind(on_press=self.search)
        self.add_widget(btn)

        scroll = ScrollView()

        self.result_layout = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None
        )
        self.result_layout.bind(minimum_height=self.result_layout.setter("height"))

        scroll.add_widget(self.result_layout)
        self.add_widget(scroll)

    def search(self, instance):
        self.result_layout.clear_widgets()

        try:
            score = float(self.score_input.text)
        except:
            return

        schools = DISTRICT_DATA[self.district.text]["学校"]

        for s in schools:
            diff = score - s["min_score"]

            if diff >= 10:
                advice = "保底"
            elif diff >= 0:
                advice = "稳妥"
            else:
                advice = "冲刺"

            self.result_layout.add_widget(Card(s, advice))

class ZhongkaoApp(App):
    def build(self):
        return Root()

if __name__ == "__main__":
    ZhongkaoApp().run()
