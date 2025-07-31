from manim import *
from scipy.stats import norm
import numpy as np

class PowerVsN(Scene):
    def construct(self):
        mu_0 = 0
        sigma = 1.5
        alpha = 0.05
        x_min = -1
        x_max = 5.5

        x_length = 9
        y_length = 3

        ns = [10, 30, 50, 100, 200, 500]
        colors = [YELLOW, GREEN, ORANGE, PURPLE, TEAL, BLUE]

        axes = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[0, 1.05, 1],
            x_length=x_length,
            y_length=y_length,
            axis_config={"color": WHITE, "include_tip": False},
            y_axis_config= {
                "numbers_to_include": [1],
                "label_direction": LEFT,
            },
            x_axis_config= {
                "include_ticks": False,
                "include_numbers": False,
            }
        )

        # Axis labels
        mu_label = MathTex(r"\mu", color=WHITE).next_to(axes.x_axis, RIGHT, buff=0.3)
        power_label = MathTex(r"\text{Power}", color=WHITE).next_to(axes.y_axis, LEFT, buff=0.3).shift(UP*1.4)

        mu0_label = MathTex(r"\mu_0", color=WHITE).next_to(axes.c2p(mu_0, 0), DOWN, buff=0.3)
        axes_labels = VGroup(mu_label, power_label, mu0_label)

        self.add(axes, axes_labels)
        
        lines = []
        legend_labels = []

        for i, n in enumerate(ns):
            se = sigma / np.sqrt(n)
            c_n = norm.ppf(1 - alpha, loc=mu_0, scale=se)

            def power(mu_, c_val=c_n, s_val=se):
                return 1 - norm.cdf(c_val, loc=mu_, scale=s_val)

            graph = axes.plot(
                lambda mu_: power(mu_),
                x_range=[x_min, x_max, 0.01],
                color=colors[i],
                stroke_width=6,
                use_smoothing=False,
            )

            # Animate curve and legend label
            n_label = MathTex(f"n={n}", color=colors[i]).scale(0.8)
            if legend_labels:
                n_label.next_to(legend_labels[-1], DOWN, aligned_edge=LEFT, buff=0.18)
            else:
                n_label.to_corner(UR).shift(DOWN*1 + LEFT*0.4)
            self.play(Create(graph), Create(n_label), run_time=1.0)
            self.add(graph, n_label)
            lines.append(graph)
            legend_labels.append(n_label)
            self.wait(0.5)

        # Remove all finite-n curves and legend
        self.play(*[Uncreate(line) for line in lines], *[Uncreate(lbl) for lbl in legend_labels])
        self.wait(0.5)

        # n = infinity: step function, sequential line appearance, no jump
        left_inf = axes.plot(lambda mu_: 0, x_range=[x_min, mu_0], color=WHITE, stroke_width=7)
        right_inf = axes.plot(lambda mu_: 1, x_range=[mu_0, x_max], color=WHITE, stroke_width=7)
        inf_label = MathTex(r"n=\infty", color=WHITE).scale(0.8)
        inf_label.to_corner(UR).shift(DOWN*1.0 + LEFT*0.4)

        # Show both the first (y=0) segment and the label together
        self.play(Create(left_inf), Create(inf_label))
        self.wait(0.4)
        # Now animate the right (y=1) segment
        self.play(Create(right_inf))
        self.wait()