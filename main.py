from manim import * 
from manim.mobject.svg.svg_mobject import SVGMobject
from manim_slides import Slide

screen_width = 16/9 * 8

config.background_color = "#fcfbf1"
black_color = "#323030"
blue_color = "#6883FB"
red_color = "#F1534D"
green_color = "#5CB85C"
head_color = "#fcad63"

Text.set_default(color = black_color)
Tex.set_default(color = black_color)
MathTex.set_default(color = black_color)
Dot.set_default(color = black_color)

class Flash(Slide):

    def fadeout_all(self, **kwargs):
        """Fade out all the currents objects from screen"""

        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
            # All mobjects in the screen are saved in self.mobjects
        )

    def remove_all(self, **kwargs):
        """Remove all the currents objects from screen"""

        self.remove(*self.mobjects)

    

    def construct(self):

        texTemplate = TexTemplate()
        texTemplate.add_to_preamble(r"\usepackage{physics, amsmath, amssymb}")
        
        self.wait(0.1)
        self.next_slide()
        self.remove_all()

        # -----------------------------------------------
        #                  TITLE SCREEN
        # -----------------------------------------------
        
        title = Text(r"Floquet Theory applied to Lindbladian Open Quantum Systems")
        authors = Text(r"Antonio de la M. Sojo López", use_svg_cache=True).scale(0.7)

        # Logos 'n' stuff
        logo_us = ImageMobject("./assets/logos/logo_us.png").scale_to_fit_height(1)
        banner_min = ImageMobject("./assets/logos/min_banner.jpg").scale_to_fit_height(1)
        banners = Group(
            Group(
                logo_us,
                Text("PIF VII Plan Propio").scale_to_fit_width(logo_us.width)\
                    .next_to(logo_us, DOWN, buff=0.1)
            ),
            Group(
                banner_min,
                Text("PID2022-136228NB-C22").scale_to_fit_width(banner_min.width)\
                    .next_to(banner_min, DOWN, buff=0.1)
            )
        ).arrange(RIGHT, buff = 0.5).scale_to_fit_height(1.5)

        title_screen = VGroup(
            title,
            authors,
        ).scale_to_fit_width(0.85*screen_width).arrange(DOWN, buff=0.35)
        authors.shift(0.15*DOWN)
        banners.to_edge(DOWN, buff = 0.5)

        self.play(
            Write(title)
        )
        self.play(
            Write(authors),
            FadeIn(banners, shift = UP)
        )

        # -----------------------------------------------
        #                 Floquet Theory
        # -----------------------------------------------

        self.next_slide()
        self.remove_all()

        title_floquet = Title("Floquet Theory", include_underline=False)

        floquet_table = MobjectTable(
            [
                [MathTex(r"\ket{\Psi}\in\mathcal{H}", tex_template=texTemplate), MathTex(r"\rho\in L(\mathcal{H})", tex_template=texTemplate)],
                [MathTex(r"\dv{}{t}\ket{\Psi} = -\frac{i}{\hbar}H(t)\ket{\Psi}", tex_template=texTemplate), MathTex(r"\dv{}{t}\rho = \mathcal{L}(t)\rho", tex_template=texTemplate)],
                [MathTex(r"U(t,t_0) \in U(n)"), MathTex(r"\mathcal{E}(t,t_0) \in \text{CPTP Map}")],
                [
                    VGroup(
                        MathTex(r"H(t+T) = H(t)"),
                        MathTex(r"U(t,t_0) = P(t,t_0)e^{-\frac{i}{\hbar}(t-t_0)H_\text{eff}}"),
                        Tex(r"$H_\text{eff}$ is Hermitian")
                    ).arrange(DOWN, buff = 0.3),
                    VGroup(
                        MathTex(r"\mathcal{L}(t+T) = \mathcal{L}(t)"),
                        MathTex(r"\mathcal{E}(t,t_0) = \mathcal{P}(t,t_0)e^{(t-t_0)\mathcal{G}_\text{eff}}"),
                        Tex(r"$\mathcal{G}_\text{eff}$ is ???")
                    ).arrange(DOWN, buff = 0.3)
                ]
            ],
            col_labels=[Text("Closed"), Text("Open Lindbladian")],
            row_labels=[Text("State"), Text("Evolution"), Text("Propagator"), Text("Floquet")],
            line_config = {"color": black_color}
        ).scale_to_fit_width(screen_width).shift(0.5*DOWN)
        floquet_table.remove(*floquet_table.get_horizontal_lines())

        footnotes = Tex(r"$U(n)\equiv$ Unitary Group; CPTP $\equiv$ Completely Positive Trace Preserving Map")\
        .scale(0.7).next_to(floquet_table, DOWN, buff = 0.35)

        slide = VGroup(
            title_floquet,
            floquet_table,
            footnotes
        ).scale_to_fit_height(7.5).center()
        
        self.play(
            Write(title_floquet),
            Write(floquet_table.get_col_labels()),
            Write(floquet_table.get_row_labels()),
            Create(floquet_table.get_vertical_lines()),
            Write(footnotes)
        )
        
        for row in floquet_table.get_rows()[1:]:
            self.next_slide()
            self.play(Write(row[1:]))

        self.next_slide()
        self.play(
            Transform(
                floquet_table.get_rows()[-1][1],
                Tex(r"$H_\text{eff}$ is Hermitian").scale(1).set_color(green_color).move_to(floquet_table.get_rows()[-1][1])
            )
        )

        self.next_slide()
        self.play(
            Transform(
                floquet_table.get_rows()[-1][2],
                Tex(r"$\mathcal{G}_\text{eff}$ is ???").scale(1.5).set_color(red_color).move_to(floquet_table.get_rows()[-1][2])
            )
        )


        # -----------------------------------------------
        #        Problem Statement and current solution
        # -----------------------------------------------

        self.next_slide()
        self.remove_all()

        title_problem = Title("Is the Floquet Generator a Lindbladian?")
        title_problem.underline.color = black_color

        cptp_rect = Rectangle(height = 5.5, width = 8.5, color = blue_color, fill_color = blue_color, fill_opacity=0.1)
        cptp_title = Tex(r"CPTP", color = blue_color).scale_to_fit_height(0.35).move_to(cptp_rect.get_top() + 0.35*DOWN)
        cptp_math = MathTex(r"\mathcal{E} = \mathcal{T}e^{\int d\tau \mathcal{L}(\tau)}", color = blue_color)\
            .scale_to_fit_height(0.5)
        cptp_set = VGroup(
            cptp_title,
            cptp_math,
            cptp_rect
        ).set_z_index(1)

        ticptp_rect = Rectangle(height = 4, width = 4, color = green_color, fill_color = green_color, fill_opacity=0.1)
        ticptp_title = Tex(r"Time Indp. $\mathcal{L}$ CPTP", color = green_color).scale_to_fit_height(0.3).move_to(ticptp_rect.get_top() + 0.35*DOWN)
        ticptp_math = MathTex(r"\mathcal{E} = e^{t\mathcal{L}}", color = green_color)\
            .scale_to_fit_height(0.5).move_to(ticptp_rect.get_center())
        
        ticptp_set = VGroup(
            ticptp_title,
            ticptp_math,
            ticptp_rect
        ).shift(2*RIGHT+0.5*DOWN).set_z_index(2)

        cptp_math.move_to(ticptp_rect.get_center()).shift(2*ticptp_rect.get_center()[0]*LEFT)
        ticptp_math.shift(0.5*UP)

        uni_rect = Rectangle(height = 1.75, width = 3, color = red_color, fill_color = red_color, fill_opacity=0.1)
        uni_title = Tex(r"Unitary", color = red_color).scale_to_fit_height(0.35).move_to(uni_rect.get_top() + 0.35*DOWN)
        uni_math = MathTex(r"U = e^{itH}", color = red_color)\
            .scale_to_fit_height(0.5).move_to(uni_rect.get_center()+0.15*DOWN)
        
        uni_set = VGroup(
            uni_title,
            uni_math,
            uni_rect
        ).shift(ticptp_set.get_center()+1*DOWN).set_z_index(3)

        tdcptp_title = Tex(r"Time Dep. $\mathcal{L}$ CPTP", color = blue_color).scale_to_fit_height(0.3)\
            .move_to(ticptp_rect.get_top() + 0.35*DOWN).shift(2*ticptp_title.get_x()*LEFT)

        sets = VGroup(cptp_set, ticptp_set, uni_set, tdcptp_title).shift(0.5*DOWN)
        
        self.play(Write(title_problem))
        self.play(Create(uni_rect), Write(uni_title), Write(uni_math))
        
        self.next_slide()
        self.play(Create(cptp_rect), Write(cptp_title), Write(cptp_math))

        self.next_slide()
        self.play(Create(ticptp_rect), Write(ticptp_title), Write(ticptp_math), Write(tdcptp_title))
        

        text1 = Tex(r"Necessary and sufficient conditions given by [Wolf et al. 2008]")
        text2 = Tex(r"Hard to use analytically", r" $\rightarrow$ ", r"Propose solvable models")
        text2[0].set_color(red_color)
        text2[2].set_color(green_color)
        text3 = Tex(r"Inconclusive results numerically [Schnell et al. 2020]", r" $\rightarrow$ ", r"Find new conditions")
        text3[0].set_color(red_color)
        text3[2].set_color(green_color)
        text4 = Tex(r"Only valid for Diagonalizable cases", r" $\rightarrow$ ", r"Generalize it. Symmetries")
        text4[0].set_color(red_color)
        text4[2].set_color(green_color)

        wolf_data = VGroup(
            text1.to_edge(LEFT, buff = 0.5),
            text2.to_edge(LEFT, buff = 1),
            text3.to_edge(LEFT, buff = 1),
            text4.to_edge(LEFT, buff = 1)
        ).arrange(DOWN, buff = 0.35, center=False).scale_to_fit_width(13).to_edge(LEFT, buff = 0.5).to_edge(DOWN, buff = 0.5)

        text1.shift(0.25*UP)
        under1 = Underline(text1).set_color(black_color)

        self.next_slide()
        self.play(
            sets.animate.move_to(0.2*sets.height*UP).scale(0.5),
            Write(wolf_data[0]), Create(under1)
        )

        for obj in wolf_data[1:]:
            self.next_slide()
            self.play(Write(obj))

        # -----------------------------------------------
        #              Floquet Engineering
        # -----------------------------------------------

        self.next_slide()
        self.remove_all()

        title_engine = Title("Floquet Engineering")   
        title_engine.underline.color = black_color

        text1 = Tex(r"By tuning the parameters of a periodic driving $V(t)$")
        eq1 = MathTex(r"H(t) = H_0 + V(t)")
        text2 = Tex(r"we can ``engineer'' an effective Hamiltonian $H_{\text{eff}}$ with \\ desirable properties.", tex_environment="flushleft")
        text3 = Tex(r"At stroboscopic times $t_0 + kT$ the system behaves as \\ we wanted:", tex_environment="flushleft")
        eq2 = MathTex(r"U(t_0+kT, t_0) = e^{-i\frac{kT}{\hbar}H_F}")
        text4 = Tex(r"It is useful to extend this to \textbf{Lindbladian} systems").scale(1.2).set_color(green_color)
        VGroup(text1, eq1, text2, text3, eq2, text4).arrange(DOWN, buff=0.5).scale_to_fit_height(5.5).to_edge(DOWN, buff = 0.5)
        text1.to_edge(LEFT, buff = 1)
        text2.to_edge(LEFT, buff = 1)
        text3.to_edge(LEFT, buff = 1)
        
        self.play(Write(title_engine))
        self.play(Write(text1), Write(eq1), Write(text2))

        self.next_slide()
        self.play(Write(text3), Write(eq2))
        
        self.next_slide()
        self.play(Write(text4))
        
        # -----------------------------------------------
        #                   Bye Bye
        # -----------------------------------------------

        self.next_slide()
        self.remove_all()

        end_slide = VGroup(
            Tex(r"Thank you for your attention! \\ Any questions?").scale(1.25),
            VGroup(
                Tex(r"\textbf{[Wolf et al. 2008]}").scale(0.8),
                Tex(r"Wolf, M., Eisert, J., Cubitt, T., \& Cirac, J. (2008).\\ \textit{Assessing Non-Markovian Quantum Dynamics} Phys. Rev. Lett., 101, 150402.", tex_environment="flushleft").scale(0.8),
                Tex(r"\textbf{[Schnell et al. 2020]}").scale(0.8),
                Tex(r"Schnell, A., Eckardt, A., \& Denisov, S. (2020).\\ \textit{Is there a Floquet Lindbladian?} Phys. Rev. B, 101, 100301.", tex_environment="flushleft").scale(0.8),
            ).arrange_in_grid(3, 2, buff = 0.5, cell_alignment=LEFT).scale_to_fit_width(13)
        ).arrange(DOWN, buff = 1)

        self.play(Write(end_slide))
        self.wait(0.1)

        # -----------------------------------------------
        #                   EXTRAS
        # -----------------------------------------------

        self.next_slide()
        self.remove_all()