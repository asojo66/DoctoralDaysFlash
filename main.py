from manim import * 
from manim.mobject.svg.svg_mobject import SVGMobject
from manim_slides import Slide

screen_width = 16/9 * 8

config.background_color = "#fcfbf1"
black_color = "#323030"
blue_color = "#6883FB"
red_color = "#F1534D"
green_color = "#5CB85C"
yellow_color = "#ff6f1b"
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
        
        doctoral_days = Text("Doctoral Days. March 13, 2025").scale(1.1).to_edge(UP, buff = 0.5)
        title = Text(r"Floquet Theory applied to Lindbladian Open Quantum Systems")
        authors = VGroup(
            Text(r"Antonio de la M. Sojo López").scale(0.7),
            Text(r"Supervisor: Jesús Casado Pascual").scale(0.7)
        ).arrange(DOWN, buff = 0.15)

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
            FadeIn(doctoral_days, shift = DOWN),
            Write(authors),
            FadeIn(banners, shift = UP)
        )

        # -----------------------------------------------
        #                 Floquet Theory
        # -----------------------------------------------

        self.next_slide()
        self.remove_all()

        title_floquet = Title("Motivation", include_underline=False)

        ev_eq_u = MathTex(r"\dv{}{t}\ket{\Psi(t)} = -\frac{i}{\hbar}H(t)\ket{\Psi(t)}", tex_template=texTemplate)
        ev_eq_L = MathTex(r"\dv{}{t}\rho(t) = \mathcal{L}(t)\rho(t)", tex_template=texTemplate)
        prop_U = MathTex(r"\ket{\Psi(t)} = U(t,t_0)\ket{\Psi(t_0)} \text{ (Unitary)}", tex_template=texTemplate)
        prop_L = MathTex(r"\rho(t_0)=\mathcal{E}(t,t_0)\rho(t_0) \text{ (CPTP Map)}", tex_template=texTemplate)
        periodic_row = [Tex(r"If $H(t+T) = H(t)$"), Tex(r"If $\mathcal{L}(t+T) = \mathcal{L}(t)$")]
        stroboscopic = [
                    MathTex(r"U(nT, 0) = ", r"e^{-\frac{i}{\hbar}nT H_\text{eff}}"),
                    MathTex(r"\mathcal{E}(nT, 0) = ", r"e^{nT \mathcal{G}_\text{eff}}")
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

        footnotes = Tex(r"CPTP $\equiv$ Completely Positive Trace Preserving Map")\
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
                .next_to(connection_U[-1], LEFT, buff = 0).shift(0.15*DOWN+0.1*RIGHT)
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
            Text("Floquet Engineering?").scale(0.4).set_color(red_color)\
                .next_to(connection_L[-1], LEFT, buff = 0).shift(0.15*DOWN+0.1*RIGHT)
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

        cptp_rect = Rectangle(height = 5.5, width = 9, color = blue_color, fill_color = blue_color, fill_opacity=0.1)
        cptp_title = Tex(r"CPTP", color = blue_color).scale_to_fit_height(0.35).move_to(cptp_rect.get_top() + 0.35*DOWN)
        cptp_rect.set_z_index(1)
        cptp_title.set_z_index(1)
        cptp_set = VGroup(
            cptp_title,
            cptp_rect
        )

        linbladian_rect = Rectangle(height = 4.25, width = 0.6*11, color = yellow_color, fill_color = yellow_color, fill_opacity=0.1)\
            .shift(cptp_rect.width/8*RIGHT+0.5*DOWN)
        linbladian_title = Tex(r"Lindbladian $\mathcal{L}$", color = yellow_color).scale_to_fit_height(0.35).move_to(linbladian_rect.get_top() + 0.35*DOWN)
        linbladian_rect.set_z_index(2)
        linbladian_title.set_z_index(2)
        linbladian_set = VGroup(
            linbladian_title,
            linbladian_rect
        )

        TD_rect = Rectangle(height = 3, width = 0.25*11, color = green_color, fill_color = green_color, fill_opacity=0.1)\
            .shift(cptp_rect.width/8*RIGHT-linbladian_rect.width/4*RIGHT+1*DOWN)
        TD_title = VGroup(
            Tex(r"Non-Constant Gen.", color = green_color).scale(0.85),
            MathTex(r"\mathcal{T}e^{\int d\tau\mathcal{L}(\tau)}", color = green_color)
        ).arrange(DOWN, buff = 0.2).scale_to_fit_height(0.8).scale_to_fit_height(0.8).move_to(TD_rect.get_top() + 0.55*DOWN)
        TD_rect.set_z_index(3)
        TD_title.set_z_index(3)
        TD_set = VGroup(
            TD_title,
            TD_rect
        )

        ITD_rect = Rectangle(height = 3, width = 0.25*11, color = green_color, fill_color = green_color, fill_opacity=0.1)\
            .shift(cptp_rect.width/8*RIGHT+linbladian_rect.width/4*RIGHT+1*DOWN)
        ITD_title = VGroup(
            Tex(r"Constant Gen.", color = green_color),
            MathTex(r"e^{t\mathcal{L}}", color = green_color)
        ).arrange(DOWN, buff = 0.2).scale_to_fit_height(0.8).move_to(ITD_rect.get_top() + 0.55*DOWN)
        ITD_rect.set_z_index(3)
        ITD_title.set_z_index(3)
        ITD_set = VGroup(
            ITD_title,
            ITD_rect
        )

        uni_rect = Rectangle(height = 1.5, width = 2, color = red_color, fill_color = red_color, fill_opacity=0.1)\
            .move_to(ITD_rect).shift(0.5*DOWN)
        uni_title = Tex(r"Unitary", color = red_color).scale_to_fit_height(0.35).move_to(uni_rect)
        uni_rect.set_z_index(4)
        uni_title.set_z_index(4)
        uni_set = VGroup(
            uni_title,
            uni_rect
        )

        sets = VGroup(cptp_set, linbladian_set, TD_set, ITD_set, uni_set).shift(0.5*DOWN)
        
        self.play(Write(title_problem), FadeIn(cptp_set))
        self.wait(0.3)
        self.next_slide()
        self.play(FadeIn(linbladian_set))
        self.wait(0.3)
        self.next_slide()
        self.play(FadeIn(TD_set),FadeIn(ITD_set)) 
        #self.play(FadeIn(ITD_set))
        self.wait(0.3)
        self.next_slide()
        self.play(FadeIn(uni_set))
        self.wait(0.3)

        self.next_slide(loop = True)

        loop_set = VGroup(ITD_set, uni_set)
        
        self.play(loop_set.animate.scale(1.1), title_problem.animate.scale(1.1))
        self.play(loop_set.animate.scale(1/1.1), title_problem.animate.scale(1/1.1))

        self.next_slide()
        text1 = Tex(r"Necessary and sufficient conditions given by [1]")
        text2 = Tex(r"Hard to use analytically", r" $\rightarrow$ ", r"Let's propose solvable models")
        text2[0].set_color(red_color)
        text2[2].set_color(green_color)
        text3 = Tex(r"Inconclusive results numerically [2]", r" $\rightarrow$ ", r"Let's find better criteria")
        text3[0].set_color(red_color)
        text3[2].set_color(green_color)
        text4 = Tex(r"Only valid for diagonalizable cases", r" $\rightarrow$ ", r"Let's generalize it. Symmetries")
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

        refs = VGroup(
                Tex(r"\textbf{[1]}").scale(0.8),
                Tex(r"Wolf, M., Eisert, J., Cubitt, T., \& Cirac, J. (2008).\\ \textit{Assessing Non-Markovian Quantum Dynamics.}\\ Phys. Rev. Lett., 101, 150402.", tex_environment="flushleft").scale(0.8),
                Tex(r"\textbf{[2]}").scale(0.8),
                Tex(r"Schnell, A., Eckardt, A., \& Denisov, S. (2020).\\ \textit{Is there a Floquet Lindbladian?}\\ Phys. Rev. B, 101, 100301.", tex_environment="flushleft").scale(0.8),
            ).arrange_in_grid(3, 2, buff = 0.5, cell_alignment=UP).scale_to_fit_height(0.4*sets.height)\
            
        sets_and_refs = VGroup(sets.copy().scale(0.5), refs).center().arrange(RIGHT, buff = 0.5).next_to(title_problem, DOWN, buff = 0.25)

        self.next_slide()
        self.play(
            sets.animate.move_to(sets_and_refs[0]).scale(0.5),
            Write(refs),
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

        end_slide = Tex(r"Thank you for your attention! \\ Any questions?").scale(1.25)

        self.play(Write(end_slide))
        self.wait(0.1)

        # -----------------------------------------------
        #                   EXTRAS
        # -----------------------------------------------

        self.next_slide()
        self.remove_all()

        title_floquet_ext = Title("Floquet Theorem")
        title_floquet_ext.underline.color = black_color

        text1 = Tex(r"Consider the system of linear diff. equations for $M(t)\in\mathcal{M}_n(\mathbb{C})$")
        system = MathTex(r"\frac{d}{dt}M(t) = C(t)M(t);\quad M(0) = I_n;\qquad C(t)\in\mathcal{M}_n(\mathbb{C})")
        text2 = Tex(r"If $M(t) = M(t+T)$ for some fixed $T\in\mathbb{R}$, then:")
        floquet = MathTex(r"M(t) = P(t)e^{t G}\text{ with } P(t) = P(t+T)")

        floquetslide = VGroup(text1, system, text2, floquet).arrange(DOWN, buff = 0.5)

        self.add(
            title_floquet_ext,
            floquetslide
        )

        self.wait(1)

        self.next_slide()
        self.remove_all()

        title_cp = Title("Completely Positive Maps")
        title_cp.underline.color = black_color

        big_sys = Ellipse(8, 4, color = red_color, fill_color = red_color, fill_opacity = 1)
        im_sys = Ellipse(4, 3, color = blue_color, fill_color = blue_color, fill_opacity = 1).shift(1.5*RIGHT)

        eq = MathTex(r"\mathcal{E}",r"\otimes", r"\mathcal{I}_\text{n}", r"\text{ must map density matrices to density matrices}").next_to(big_sys, DOWN, buff = 1)
        eq[0].set_color(blue_color)
        eq[2].set_color(red_color)

        self.add(
            title_cp,
            big_sys, 
            im_sys,
            Text("System").scale(0.5).move_to(im_sys),
            Text(r"Ancilla System").scale(0.5).move_to(big_sys).shift(2*LEFT),
            eq
        )

        self.wait(1)

        self.next_slide()
        self.remove_all()
