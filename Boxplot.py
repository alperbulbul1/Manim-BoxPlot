from manim import *
import numpy as np

class SeabornBoxPlotScene(Scene):
    def construct(self):
        # Example data (You should replace these with your actual computed values)
        categories = ["Cat1", "Cat2", "Cat3"]
        subcat1_data = {
            "Cat1": (-1, -0.5, 0, 0.5, 1),  # (min, Q1, median, Q3, max)
            "Cat2": (-1.5, -1, 0, 1, 1.5),
            "Cat3": (-2, -0.75, 0.5, 0.75, 2),
        }
        subcat2_data = {
            "Cat1": (-1.2, -0.6, 0.1, 0.6, 1.2),
            "Cat2": (-1.4, -0.9, 0.2, 1.1, 1.6),
            "Cat3": (-1.8, -0.7, 0.6, 0.8, 2.1),
        }

        subcat1_points = {
            "Cat1": [-0.8, -0.4, 0.2, 0.4, 0.9],
            "Cat2": [-1.3, -0.9, 0.1, 0.9, 1.4],
            "Cat3": [-1.9, -0.7, 0.6, 0.7, 1.9],
        }
        subcat2_points = {
            "Cat1": [-1.1, -0.5, 0.3, 0.5, 1.1],
            "Cat2": [-1.2, -0.8, 0.3, 1.0, 1.5],
            "Cat3": [-1.7, -0.6, 0.7, 0.8, 2.0],
        }

        box_width = 0.3
        spacing = 1.2  # Spacing between family groups
        group_spacing = 0.3  # Spacing between case and control within a group

        # Create axes
        axes = Axes(
            x_range=[0, len(categories) * spacing, spacing],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": BLUE, "include_numbers": True, 'numbers_to_include':[-3,-2,-1,0,1,2,3]},
        ).to_edge(DOWN, buff=1)
        axes.get_x_axis().set_opacity(0)
        self.play(Create(axes))

        # Add family IDs under the x-axis
        cats_v = VGroup()
        for i, cat in enumerate(categories):
            cat_label = Text(cat, font_size=10).next_to(axes.c2p(i+1 * spacing, -3), DOWN)
            cats_v.add(cat_label)
        self.play(Write(cats_v))

        # Function to create a boxplot
        def create_boxplot(data, x_pos, color, label):
            min_val, q1, median, q3, max_val = data
            box = Rectangle(
                width=box_width,
                height=axes.y_length * (q3 - q1) / 6,  # Assuming y_range of 6 units
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.5,
            ).move_to(axes.c2p(x_pos, (q1 + q3) / 2))

            lower_whisker = Line(
                start=axes.c2p(x_pos, q1),
                end=axes.c2p(x_pos, min_val)
            )
            lower_whisker_hor = Line(
                start=axes.c2p(x_pos - box_width / 8, min_val),
                end=axes.c2p(x_pos + box_width / 8, min_val)
            )
            upper_whisker_hor = Line(
                start=axes.c2p(x_pos, q3),
                end=axes.c2p(x_pos, max_val)
            )

            upper_whisker = Line(
                start=axes.c2p(x_pos - box_width / 8, max_val),
                end=axes.c2p(x_pos + box_width / 8, max_val)
            )

            median_line = Line(
                start=axes.c2p(x_pos - box_width / 6, median),
                end=axes.c2p(x_pos + box_width / 6, median)
            )
            lab = Text(label, font_size=10).next_to(lower_whisker, DOWN)
            return VGroup(box, lower_whisker, lower_whisker_hor, upper_whisker, upper_whisker_hor, median_line, lab)

        # Plotting each boxplot
        dots = VGroup()
        boxes = VGroup()
        for i, cat in enumerate(categories):
            case_group = create_boxplot(subcat1_data[cat], i+1 * spacing - group_spacing / 2, RED, 'SubCat1')
            control_group = create_boxplot(subcat2_data[cat], i+1 * spacing + group_spacing / 2, GREEN, 'SubCat1')
            boxes.add(case_group)
            boxes.add(control_group)


            for value in subcat1_points[cat]:
                dot = Dot(color=RED).move_to(axes.c2p(i + 1 * spacing - group_spacing / 2, value))
                dots.add(dot)

            # Plot control points
            for value in subcat2_points[cat]:
                dot = Dot(color=GREEN).move_to(axes.c2p(i + 1  * spacing + group_spacing / 2, value))
                dots.add(dot)
        self.play(Create(boxes), run_time=1)
        self.play(FadeIn(dots, scale=0.5), run_time=1)

        self.wait(2)
