from manim import *
import numpy as np

class Everything(Scene):
    def construct(self):
        Title.construct(self)
        Setup.construct(self)
        SmallTimestep.construct(self)

class Title(Scene):
    def construct(self):
        title = Text("Kepler's first law derivation")
        self.wait(0.5)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))


class Setup(Scene):
    def construct(self):
        sun = SVGMobject("res/sun.svg", height=0.8)
        self.play(FadeIn(sun))

        points = [
            np.array([3, -2, 0]),
            np.array([2, 2, 0]),
            np.array([-1, -4, 0]),
            np.array([3, 0, 0]),
        ]

        earth = SVGMobject("res/earth.svg", height=0.4)
        earth.move_to(points[0])
        self.play(FadeIn(earth))

        path = CubicBezier(*points) 
        r = Line()
        r.add_updater(lambda r: r.put_start_and_end_on(sun.get_center(), earth.get_center()))

        v = Arrow(start=earth.get_center(), end=earth.get_center()+[0.5,0.5,0], color=RED, max_tip_length_to_length_ratio=0.8)
        v.put_start_and_end_on(earth.get_center(), earth.get_center()+[0.5,0.5,0])
        def update_v(v):
            angle = TangentLine(path, proportions_along_bezier_curve_for_point(earth.get_center(), points)).get_angle()
            v.put_start_and_end_on(earth.get_center(), earth.get_center() + [v.get_length()*np.cos(angle), v.get_length()*np.sin(angle), 0])
        v.add_updater(update_v)

        self.play(MoveAlongPath(earth, path, rate_func=smooth, run_time = 3), FadeIn(r), FadeIn(v))
        self.wait(0.5)

        # introduce variables
        theta_base = DashedLine(earth.get_center(), earth.get_center()+[1,0,0], color=BLUE)
        theta = Angle(r, v, radius=0.4, color=BLUE)
        theta_symbol = MathTex("\\theta").scale(0.6).set_color(BLUE)
        theta_symbol.move_to(theta)
        theta_symbol.shift(0.2*RIGHT+0.1*UP)
        r_symbol = MathTex("r").scale(0.6)
        r_symbol.move_to(r)
        r_symbol.shift(0.2*DOWN)
        v_symbol = MathTex("v").scale(0.6).set_color(RED)
        v_symbol.move_to(v)
        v_symbol.shift(0.2*RIGHT+0.45*UP)
        self.play(Create(theta), Create(theta_base), Create(theta_symbol), Create(r_symbol), Create(v_symbol))
        self.wait(1)

        r.clear_updaters()
        v.clear_updaters()


class SmallTimestep(Scene):
    def construct(self):
        # setup
        sun = SVGMobject("res/sun.svg", height=0.8)
        earth = SVGMobject("res/earth.svg", height=0.4)
        earth.move_to(np.array([3, 0, 0]))
        v = Arrow(start=earth.get_center(), end=earth.get_center()+[0.5,0.5,0], color=RED, max_tip_length_to_length_ratio=0.8)
        v.put_start_and_end_on(earth.get_center(), earth.get_center()+[0.5,0.5,0])
        v.set_z_index(1)
        r = Line(sun.get_center(), earth.get_center())
        g = Group(sun, earth, v, r)
        self.add(g)
        theta_base = DashedLine(earth.get_center(), earth.get_center()+[1,0,0], color=BLUE)
        theta = Angle(r, v, radius=0.4, color=BLUE)
        theta_symbol = MathTex("\\theta").scale(0.6).set_color(BLUE)
        theta_symbol.move_to(theta)
        theta_symbol.shift(0.2*RIGHT+0.1*UP)
        r_symbol = MathTex("r").scale(0.6)
        r_symbol.move_to(r)
        r_symbol.shift(0.2*DOWN)
        v_symbol = MathTex("v").scale(0.6).set_color(RED)
        v_symbol.move_to(v)
        v_symbol.shift(0.2*RIGHT+0.45*UP)
        self.add(theta, theta_base, theta_symbol, r_symbol, v_symbol)

        # text
        text = VGroup(*map(Tex, ["Consider a small timestep, $\\delta t$.", "We move a small distance $|v|\delta t$, then update the velocity vector.", "Now we mark on the changes in $v, r$ and $\\theta$."])).scale(0.5)
        text.arrange(DOWN).to_edge(LEFT).shift(UP)
        self.play(Write(text[0]))
        self.wait(0.5)
        self.play(Write(text[1]))
        self.wait(1)

        # small timestep
        _earth = earth.copy()
        _earth.set_opacity(0.3)
        self.add(_earth)
        _r = r.copy()
        _r.set(stroke_width=2)
        _r.set_color(GREY)
        _r.add_updater(lambda r: r.put_start_and_end_on(sun.get_center(), _earth.get_center()))
        self.add(_r)
        temp_v = v.copy()
        temp_v.add_updater(lambda temp_v: temp_v.put_start_and_end_on(_earth.get_center(), _earth.get_center()+[0.5,0.5,0]))
        self.add(temp_v)
        vdt = Line(stroke_width=2, color=GREY)
        vdt.add_updater(lambda vdt: vdt.put_start_and_end_on(earth.get_center(), _earth.get_center()))
        self.add(vdt)
        vdt_path = Line(earth.get_center(), earth.get_center()+[1.5, 1.5, 0])
        vdt_symbol = MathTex("|v|\\delta t").scale(0.6)
        vdt_symbol.move_to(vdt_path)
        vdt_symbol.shift(RIGHT*0.5)
        self.play(MoveAlongPath(_earth, vdt_path), Create(vdt_symbol))

        # update velocity
        _v = Arrow(start=_earth.get_center(), end=_earth.get_center()+[0.2,1,0], color=RED, max_tip_length_to_length_ratio=0.4)
        _v.put_start_and_end_on(_earth.get_center(), _earth.get_center()+[0.2,1,0])
        _v.set_z_index(1)
        self.play(ReplacementTransform(temp_v, _v))
        self.wait(1)

        #text
        self.play(Write(text[2]))
        self.wait(1)

        # introduce r+dr, v+dv
        rdr_symbol = MathTex("r + \\delta r").scale(0.6)
        rdr_symbol.move_to(_r)
        rdr_symbol.shift(LEFT*0.45+UP*0.2)
        vdv_symbol = MathTex("v + \\delta v").scale(0.6).set_color(RED)
        vdv_symbol.move_to(_v)
        vdv_symbol.shift(RIGHT*0.05+UP*0.65)
        self.play(Create(rdr_symbol), Create(vdv_symbol))
        self.wait(1)

        # introduce theta+dthteta, dalpha
        _theta_base = DashedLine(_earth.get_center(), _earth.get_center()+[np.cos(_r.get_angle()), np.sin(_r.get_angle()), 0], color=BLUE)
        _theta = Angle(_r, _v, radius=0.4, color=BLUE)
        _theta_symbol = MathTex("\\theta + \\delta\\theta").scale(0.6).set_color(BLUE)
        _theta_symbol.move_to(_theta)
        _theta_symbol.shift(0.45*RIGHT+0.25*UP)
        alpha = Angle(r, _r, radius=1, color=BLUE)
        alpha_symbol = MathTex("\\delta\\alpha").scale(0.6).set_color(BLUE)
        alpha_symbol.move_to(alpha)
        alpha_symbol.shift(0.35*RIGHT+0.1*UP)
        self.play(Create(_theta), Create(_theta_base), Create(_theta_symbol), Create(alpha), Create(alpha_symbol))
        self.wait(1)

        self.play(Uncreate(text[0]), Uncreate(text[2]), ApplyMethod(text[1].to_edge, LEFT+UP))
        self.wait(1)