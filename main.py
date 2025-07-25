from manim import *
from scipy.stats import norm

class PowerBeta(Scene):
    def construct(self):
        mu_0 = 0
        sigma = 1.5
        alpha = 0.05
        c = norm.ppf(1 - alpha, loc=mu_0, scale=sigma)
        mu_a_target = c - sigma * norm.ppf(0.05)

        # x-range for both main and power subplot
        x_min = -mu_a_target - 5
        x_max = mu_a_target + 5

        # Main distribution axes (same as before)
        axes = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[0, 0.3, 0.1],
            x_length=9,
            y_length=3,
            axis_config={"color": WHITE, "include_tip": False, "include_ticks": False},
        )

        mu_a_tracker = ValueTracker(mu_0)

        null_curve = always_redraw(
            lambda: axes.plot(lambda x: norm.pdf(x, mu_0, sigma), color=WHITE)
        )
        alt_curve = always_redraw(
            lambda: axes.plot(lambda x: norm.pdf(x, mu_a_tracker.get_value(), sigma), color=RED)
        )
        null_line = axes.get_vertical_line(axes.c2p(mu_0, 0), color=WHITE)
        alt_line = always_redraw(
            lambda: axes.get_vertical_line(axes.c2p(mu_a_tracker.get_value(), 0), color=RED)
        )
        type_ii = always_redraw(
            lambda: axes.get_area(
                axes.plot(lambda x: norm.pdf(x, mu_a_tracker.get_value(), sigma),
                          x_range=[axes.x_range[0], c]),
                color=BLUE, opacity=0.4
            )
        )
        power_area = always_redraw(
            lambda: axes.get_area(
                axes.plot(lambda x: norm.pdf(x, mu_a_tracker.get_value(), sigma),
                          x_range=[c, axes.x_range[1]]),
                color=RED, opacity=0.4
            )
        )

        null_hyp = MathTex(r"H_0:~\mu = \mu_0", color=WHITE)
        alt_hyp = MathTex(r"H_1:~\mu > \mu_0", color=RED)
        alt_hyp.next_to(null_hyp, DOWN, aligned_edge=LEFT)
        hypotheses = VGroup(null_hyp, alt_hyp).to_corner(UL).scale(0.95)


        def power_val():
            val = 1 - norm.cdf(c, loc=mu_a_tracker.get_value(), scale=sigma)
            return val

        def beta_val():
            val = norm.cdf(c, loc=mu_a_tracker.get_value(), scale=sigma)
            return val

        metrics = always_redraw(lambda:
            VGroup(
                MathTex(r"\alpha", "=", "0.05", color=WHITE),
                MathTex(r"\beta", "=", "{:.2f}".format(beta_val()), color=BLUE),
                MathTex(r"\text{Power}", "=", "{:.2f}".format(power_val()), color=RED),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            .scale(0.95)
            .next_to(hypotheses, DOWN, aligned_edge=LEFT, buff=0.5).shift(DOWN * 1.75)
        )


        # -------- Power curve subplot below --------
        # Place it just below the main axes, matching the x-alignment of mu (for vertical alignment)
        subplot_height = 2.0
        subplot_axes = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[0, 1.05, 1],
            x_length=axes.x_length,
            y_length=subplot_height,
            axis_config={"color": WHITE, "include_tip": False},
            y_axis_config={
                "color": WHITE,
                "numbers_to_include": [1]
            },
            x_axis_config={
                "color": WHITE,
                "include_ticks": False,
                "include_numbers": False
            }
        )


        subplot_axes.next_to(axes, DOWN, buff=1.4)

        # Tracking point at mu_a along x-axis
        mua_point = always_redraw(lambda: 
            Line(
                axes.c2p(mu_a_tracker.get_value(), -0.01),
                axes.c2p(mu_a_tracker.get_value(), 0.01),
                color=RED,
                stroke_width=4
            )
        )

        mua_label = always_redraw(lambda: MathTex(r"\mu_a", color=RED).next_to(
            axes.c2p(mu_a_tracker.get_value(), 0),
            DOWN,
            buff=0.2
        ))
        axes.add(null_curve, alt_curve, null_line, alt_line, type_ii, power_area, mua_point, mua_label)
        
        mu0_label = MathTex(r"\mu_0", color=WHITE).next_to(subplot_axes.c2p(mu_0, 0), DOWN, buff=0.3)


        # x label "\mu"
        mu_xlabel = MathTex(r"\mu", color=WHITE).next_to(subplot_axes.x_axis, RIGHT, buff=0.25).shift(DOWN*0.05)

        # Theoretical power function
        def power_function(mu_a):
            return 1 - norm.cdf(c, loc=mu_a, scale=sigma)
        power_curve = subplot_axes.plot(power_function, x_range=[x_min, x_max], color=WHITE)

        # Red dot tracking power at current mu_a
        power_dot = always_redraw(lambda: Dot(
            subplot_axes.c2p(mu_a_tracker.get_value(), power_function(mu_a_tracker.get_value())),
            color=RED,
            radius=0.10,
        ))
        subplot_axes.add(power_curve, power_dot, mu_xlabel)
        subplot_axes.add(mu0_label)

        plots = VGroup(axes, subplot_axes)
        plots.move_to(ORIGIN).shift(DOWN * 0.1).shift(RIGHT * 0.5)  # Center vertically


        # Add everything, order to ensure labels/dots are on top        
        self.add(
            plots,
            hypotheses,
            metrics
        )

        # Animate as before
        self.play(mu_a_tracker.animate.set_value(mu_a_target), run_time=10, rate_func=smooth)
        self.wait()
        self.play(mu_a_tracker.animate.set_value(mu_0), run_time=10, rate_func=smooth)
        self.wait()