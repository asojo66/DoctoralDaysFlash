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
highlight_color = "#fff691"

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

        title_floquet = Title("Motivation", include_underline=False)

        ev_eq_u = MathTex(r"\dv{}{t}\ket{\Psi}(t) = -\frac{i}{\hbar}H(t)\ket{\Psi}(t)", tex_template=texTemplate)
        ev_eq_L = MathTex(r"\dv{}{t}\rho(t) = \mathcal{L}(t)\rho(t)", tex_template=texTemplate)
        prop_U = MathTex(r"\ket{\Psi}(t) = U(t,t_0)\ket{\Psi}(t_0) (\in U(n))", tex_template=texTemplate)
        prop_L = MathTex(r"\rho(t_0)=\mathcal{E}(t,t_0)\rho(t_0) (\in \text{CPTP Map})", tex_template=texTemplate)
        periodic_row = [Tex(r"If $H(t+T) = H(t)$"), Tex(r"If $\mathcal{L}(t+T) = \mathcal{L}(t)$")]
        stroboscopic = [
                    MathTex(r"U(t_0+kT,t_0) = ", r"e^{-\frac{i}{\hbar}kT H_\text{eff}}"),
                    MathTex(r"\mathcal{E}(t_0+kT,t_0) = ", r"e^{kT\mathcal{G}_\text{eff}}")
        ]


        floquet_table = MobjectTable(
            [
                [MathTex(r"\ket{\Psi}\in\mathcal{H}", tex_template=texTemplate), MathTex(r"\rho\in L(\mathcal{H})", tex_template=texTemplate)],
                [
                    VGroup(
                        ev_eq_u,
                        prop_U
                    ).arrange(DOWN, buff = 0.5)
                ,
                    VGroup(
                        ev_eq_L,
                        prop_L
                    ).arrange(DOWN, buff = 0.5)
                ],
                periodic_row,
                stroboscopic
            ],
            col_labels=[Text("Closed"), Text("Open Lindbladian")],
            row_labels=[Text("State"), Text("Evolution"), Text("HOLA").set_opacity(0.0), Text("Floquet")],
            line_config = {"color": black_color}
        ).scale_to_fit_width(screen_width).shift(0.5*DOWN)
        #floquet_table.remove(*floquet_table.get_horizontal_lines())

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
            Create(floquet_table.get_horizontal_lines()),
            Write(footnotes)
        )
        
        for obj in floquet_table.get_columns()[1][1:]:
            self.next_slide()
            self.play(Write(obj))

        self.next_slide()
        
        connection_U = VGroup(
            Brace(ev_eq_u, color = red_color),
            SurroundingRectangle(stroboscopic[0][-1], color = red_color)
        )
        connection_U.add(
            Arrow(connection_U[0].get_bottom(), connection_U[-1].get_top(), buff = 0, color = red_color)
        )
        connection_U.add(
            Text("Floquet Engineering").scale(0.45).set_color(red_color)\
                .next_to(connection_U[-1], LEFT, buff = 0.1).shift(0.15*DOWN)
        )

        self.remove(periodic_row[0])
        self.play(Create(connection_U))

        self.wait(0.3)

        self.next_slide()
        self.add(periodic_row[0])
        self.remove(connection_U)
        self.play(Write(floquet_table.get_columns()[2][1]))

        for obj in floquet_table.get_columns()[2][2:-1]:
            self.next_slide()
            self.play(Write(obj))

        self.next_slide()
        self.add(floquet_table.add_highlighted_cell((5,3), color = highlight_color))
        self.play(
            Write(floquet_table.get_columns()[2][-1]))

        self.next_slide()
        
        connection_L = VGroup(
            Brace(ev_eq_L, color = red_color),
            SurroundingRectangle(stroboscopic[1][-1], color = red_color)
        )
        connection_L.add(
            Arrow(connection_L[0].get_bottom(), connection_L[-1].get_top(), buff = 0, color = red_color)
        )
        connection_L.add(
            Text("Floquet Engineering").scale(0.45).set_color(red_color)\
                .next_to(connection_L[-1], LEFT, buff = 0.1).shift(0.15*DOWN)
        )

        self.remove(periodic_row[1])
        self.play(Create(connection_L))

        self.wait(0.3)

        self.next_slide()
        self.add(periodic_row[1])
        self.remove(connection_L)

        self.play(
            Transform(
                floquet_table.get_rows()[-1][1],
                Tex(r"$H_\text{eff}$ is a Hamiltonian").scale(1).set_color(green_color).move_to(floquet_table.get_rows()[-1][1])
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