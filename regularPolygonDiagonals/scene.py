from manim import *


class Title(Scene):
    def construct(self):
        text = Text("A general case of toggling diagonals", color=BLUE)
        self.play(FadeIn(text))
        self.wait(1.5)
        self.play(FadeOut(text))


class Experimentation(Scene):
    def construct(self):
        t1 = Text("This video is about a generalized proof I came up with for Tournament of Towns Nov 1983 question 3.").scale(0.5)
        t1.align_on_border(UP)
        self.play(Write(t1))