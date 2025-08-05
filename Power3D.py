from manim import *
from scipy.stats import norm

class MuPower3DAxes(ThreeDScene):
    def construct(self):
        x_min, x_max = 0, 3
        y_min, y_max = 1, 3
        z_min, z_max = 0, 1

        axes = ThreeDAxes(
            x_range=[x_min, x_max, 1], 
            y_range=[y_min, y_max, 1], 
            z_range=[z_min, z_max, 1],
            x_length=3, 
            y_length=3,
            z_length=1,
            axis_config={
                "color": BLUE,
                "include_tip": False,
                "include_numbers": False,
                "include_ticks": False,
            }, 
            z_axis_config={
                "include_ticks": True,
                "include_tip": False,
                "color": BLUE,
            }
        )

        n = 30
        mu_0 = 0
        alpha=0.05

        x_label = axes.get_x_axis_label(Tex(r"$\mu$"), direction=UP)
        x_label.rotate(PI/2, axis=RIGHT).shift(RIGHT*0.5)
        z_label = axes.get_z_axis_label(Tex("power"), direction=UP, edge=LEFT)
        z_label.shift(OUT*0.8, LEFT*0.3)
        
        self.set_camera_orientation(phi=90 * DEGREES, theta=-90 * DEGREES, focal_distance=3)
        self.add(axes, x_label, z_label)
        self.wait(2)
        

        def power(mu_a, sigma):
            return 1 - norm.cdf(norm.ppf (1 - alpha) + (mu_0 - mu_a) / (sigma / np.sqrt(n)))

        graph = axes.plot_parametric_curve(
            lambda mu: np.array([mu, 1, power(mu, 1)]),
            t_range=[x_min, x_max, 0.01],
            stroke_width=6,
            use_smoothing=False,
            color=BLUE,
        )
        self.play(Create(graph), run_time=2)
        self.wait(2)

        #! MOVE TO 3D

        self.move_camera(phi=80 * DEGREES, theta=-85 * DEGREES, run_time=3)
        y_label = axes.get_y_axis_label(Tex(r"$\sigma$"), direction=UP, edge=LEFT)
        y_label.rotate(PI/2, axis=UP).shift(OUT*0.2 + LEFT*0.3)
        self.play(Write(y_label))
        self.wait(2)

        surface = Surface(
            lambda u, v: axes.c2p(u, v, power(u, v)),
            u_range=[x_min, x_max],
            v_range=[1, 3],
            resolution=(24, 24),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_B, BLUE_D]
        )
        self.play(Create(surface), run_time=3)
        self.wait(2)