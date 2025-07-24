from manim import *
from scipy.stats import norm

class PowerBeta(Scene):
    def construct(self):
        mu_0 = 0
        sigma = 1.5
        alpha = 0.05
        c = norm.ppf(1 - alpha, loc=mu_0, scale=sigma)

        axes = Axes(
            x_range=[-4, 7, 1],
            y_range=[0, 0.3, 0.1],
            x_length=9,
            y_length=3,
            axis_config={"color": WHITE, "include_tip": False}
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

        mu0_label = MathTex(r"\mu_0", color=WHITE).next_to(axes.c2p(mu_0, 0), DOWN, buff=0.3)
        mua_label = always_redraw(lambda: MathTex(r"\mu_a", color=RED).next_to(
            axes.c2p(mu_a_tracker.get_value(), 0),
            DOWN,
            buff=0.85  # Larger buff than mu0_label, pushes mu_a further below x-axis
        ))

        def power_val():
            val = 1 - norm.cdf(c, loc=mu_a_tracker.get_value(), scale=sigma)
            return val

        def beta_val():
            val = norm.cdf(c, loc=mu_a_tracker.get_value(), scale=sigma)
            return val

        power_tex = always_redraw(lambda: Tex(
            r"Power $= {:.2f}$".format(power_val()),
            color=RED
        ).to_corner(UR, buff=0.8).scale(1.0))

        beta_tex = always_redraw(lambda: Tex(
            r"$\beta$ $= {:.2f}$".format(beta_val()),
            color=BLUE
        ).next_to(power_tex, DOWN, aligned_edge=LEFT, buff=0.18))

        metrics = VGroup(power_tex, beta_tex)

        self.add(
            axes, null_curve, alt_curve,
            null_line, alt_line,
            type_ii, power_area,
            mu0_label, mua_label,
            hypotheses,
            metrics
        )

        self.play(mu_a_tracker.animate.set_value(3), run_time=5, rate_func=smooth)
        self.wait()
        self.play(mu_a_tracker.animate.set_value(mu_0), run_time=3, rate_func=smooth)
        self.wait()