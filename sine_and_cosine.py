from manim import *
import numpy as np
import math



##LINK TO YOUTUBE VIDEO
## https://youtu.be/j4u2vS3BfLc?si=WivwvhNYD5iI9rAq

class CreateCircle(Scene):
    def construct(self):

        #positioning and coloring functions
        def set_static_equation_colors(mobj1, mobj2, i,j):
            mobj1[i].set_color(RED)
            mobj1[j].set_color(GREEN)
            mobj2[i].set_color(RED)
            mobj2[j].set_color(YELLOW)

        #moving one object into another object
        def save_state_and_transform(copied_mobject, transform_to, i=0, j=0, is_substring=False):
            transform_from = copied_mobject.copy()
            transform_from.save_state()
            transform_from.clear_updaters()
            if is_substring == False:
                self.add(transform_from)
                self.play(Transform(transform_from, transform_to[j]))
                copied_mobject.clear_updaters()
                self.remove(transform_to[j])
                self.remove(transform_from)
            elif is_substring == True:
                self.add(transform_from[i])
                self.play(Transform(transform_from[i], transform_to[j]))
                copied_mobject.clear_updaters()
                self.remove(transform_from[i])
                self.remove(transform_to[j])

        #full cycle rotation for crucial points (minima, maxima, and 0's)
        def inspect_crucial_points():
            #parallel lines do not allow theta = 0 rotation, this is a workaround taking away line_moving
            self.play(theta_tracker.animate.set_value(1),run_time=6,rate_func=linear)
            self.remove(line_moving)
            self.play(theta_tracker.animate.set_value(0))
            self.wait(14)
            self.play(theta_tracker.animate.set_value(1))
            self.add(line_moving)

            for i in range(1,4):
                self.play(theta_tracker.animate.set_value(90*i), run_time=6,rate_func=linear)
                self.wait(14)

        #full fluid rotation of 720 degrees
        def cycle_full_rotation(my_reset_time=3, my_run_time=15):
            self.play(theta_tracker.animate.set_value(1),rate_func=linear,run_time=my_reset_time)
            self.wait(4)
            self.play(theta_tracker.animate.set_value(719),rate_func=linear,run_time=my_run_time)
            self.play(theta_tracker.animate.set_value(1),rate_func=linear,run_time=my_run_time)

        #choose quadrant to rotate to, allow random int, and whether or not to be close to crucial points
        def rotate_to_quadrant(quadrant_numeral,eliminate_near_crucial=False,my_run_time=4, my_wait_time=4,my_rate_func=smooth):            
            if eliminate_near_crucial==False:
                if quadrant_numeral == "I":
                    self.play(theta_tracker.animate.set_value(int(np.random.randint(1,90))),run_time=my_run_time,rate_func=my_rate_func)
                elif quadrant_numeral == "II":
                    self.play(theta_tracker.animate.set_value(int(np.random.randint(90,180))),run_time=my_run_time,rate_func=my_rate_func)
                elif quadrant_numeral == "III":
                    self.play(theta_tracker.animate.set_value(int(np.random.randint(180,270))),run_time=my_run_time,rate_func=my_rate_func)
                elif quadrant_numeral == "IV":
                    self.play(theta_tracker.animate.set_value(int(np.random.randint(270,359))),run_time=my_run_time,rate_func=my_rate_func)
                self.wait(my_wait_time)
            elif eliminate_near_crucial==True:
                if quadrant_numeral == "I":
                    self.play(theta_tracker.animate.set_value(int(np.random.randint(35,70))),run_time=my_run_time,rate_func=my_rate_func)
                elif quadrant_numeral == "II":
                    self.play(theta_tracker.animate.set_value(int(np.random.randint(110,160))),run_time=my_run_time,rate_func=my_rate_func)
                elif quadrant_numeral == "III":
                    self.play(theta_tracker.animate.set_value(int(np.random.randint(200,250))),run_time=my_run_time,rate_func=my_rate_func)
                elif quadrant_numeral == "IV":
                    self.play(theta_tracker.animate.set_value(int(np.random.randint(290,340))),run_time=my_run_time,rate_func=my_rate_func)
                self.wait(my_wait_time)
    
        #cycles through all quadrants
        def cycle_through_quadrants(eliminate_near_crucial=False, my_run_time=4,my_wait_time=4,my_rate_func=smooth):
            list_of_quadrants = ["I","II","III","IV"]
            for x in list_of_quadrants:
                rotate_to_quadrant(x,eliminate_near_crucial)

        #sets z indices for pairs of mobjects
        def set_pair_mobj_z_index(mobj1, mobj2, z):
            mobj1.set_z_index(z)
            mobj2.set_z_index(z)


            

            
        #defines coordinate planes,

        #axes for the circle
        axes = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            }
        ).set_z_index(0).add_coordinates()
        
        #labels for axes
        labels = axes.get_axis_labels(
            MathTex("+x"), MathTex("+y")
        )

        #axes for the graph of cosine and sine
        cosine_sub_axes = Axes(x_range=[0,720,90],
                                 y_range=[-2,2,1],
                                 x_length=5, 
                                 y_length=2,
                                 tips=False,
                                 x_axis_config={"line_to_number_buff":1.25,
                                                "include_numbers": True,
                                                "font_size":24},
                                y_axis_config={"line_to_number_buff":0.25,
                                                "include_numbers":True,
                                                "font_size":24,
                                                "numbers_to_exclude":[-1,1]}).move_to([-5,1.5,0]).scale(0.75)
        
        sine_sub_axes = Axes(x_range=[0,720,90],
                            y_range=[-2,2,1],
                            x_length=5,
                            y_length=2,
                            tips=False,
                            x_axis_config={"line_to_number_buff":1.25,
                                            "include_numbers":True,
                                            "font_size":24},
                            y_axis_config={"line_to_number_buff":0.25,
                                            "include_numbers":True,
                                            "font_size":24,
                                            "numbers_to_exclude":[-1,1]}).move_to([-5,-1.5,0]).scale(0.75)
        
        #Positioning the labels manually and scaling, then grouping since I have limited space
        cosine_sub_axes_labels = VGroup()
        cosine_graph_x_label = cosine_sub_axes.get_x_axis_label(MathTex(r"\theta").scale(0.6), edge=DOWN,direction=DOWN)
        cosine_graph_y_label = cosine_sub_axes.get_y_axis_label(MathTex(r"x").scale(0.6), edge=UP)
        cosine_sub_axes_labels.add(cosine_graph_x_label,cosine_graph_y_label)
        sine_sub_axes_labels = VGroup()
        sine_graph_x_label = sine_sub_axes.get_x_axis_label(MathTex(r"\theta").scale(0.6), edge=DOWN,direction=DOWN)
        sine_graph_y_label = sine_sub_axes.get_y_axis_label(MathTex(r"y").scale(0.6), edge=UP)
        sine_sub_axes_labels.add(sine_graph_x_label,sine_graph_y_label)


        #sets the rotation center to the center of the coordinate axes and creates a theta tracker
        rotation_center = axes.get_origin()
        theta_tracker = ValueTracker(110)

        #creates lines that start at the origin, and extend right 2 units
        line1= Line(axes.coords_to_point(0,0),2*axes.coords_to_point(1,0)).set_z_index(1)
        line_moving = Line(axes.coords_to_point(0,0),2*axes.coords_to_point(1,0))
        line_ref = line_moving.copy().set_z_index(1)

        #initialization for objects being updated
        circle = Circle().scale(2)
        circle.set_fill(RED, opacity=0.0)
        x_proj_line= Line()
        x_proj_length=Line()
        y_proj_line= Line().set_z_index(2)
        y_proj_length=Line().set_z_index(2)
        length_arrow = Arrow(start=DOWN, end=UP, color=GREEN).move_to([0,-0.75,0]).scale(0.5,scale_tips=True)
        y_length_arrow = Arrow(start=LEFT, end=RIGHT, color=YELLOW).move_to([-0.75,0,0]).scale(0.5,scale_tips=True)
        ordered_pair = Dot()
        

        #initializes the way the line moves, the angle a, and the tex, theta
        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, 
            about_point=rotation_center
        )
        a = Angle(
            line1, 
            line_moving, 
            radius=0.25, 
            other_angle=False
            )
        tex = MathTex(r"\theta").move_to(
            Angle(
                line1, line_moving, radius=0.35 + 3 * SMALL_BUFF, 
                other_angle=False
            ).point_from_proportion(0.5)
        )

        #all text and backgrounds
        big_black_background = Rectangle(height=10,
                                         width=4.2,
                                         fill_color=BLACK,
                                         fill_opacity=1.0,
                                         stroke_color=WHITE).move_to(5*RIGHT)
        
        left_big_black_background = Rectangle(height=10,
                                         width=4.7,
                                         fill_color=BLACK,
                                         fill_opacity=1.0,
                                         stroke_color=WHITE).move_to(5*LEFT)
        
        ordered_pair_background = Rectangle(height=0.75,
                                         width=1.50,
                                         fill_color=BLACK,
                                         fill_opacity=0.75,
                                         stroke_color=BLACK)
        
        ordered_pair_background.z_index=1

        #dynamic and static texts
        cosine_text = MathTex(r"cos(\theta)=\frac{x}{r}",font_size=30).move_to(big_black_background.get_center() + 0.35*UP)
        sine_text = MathTex(r"sin(\theta)=\frac{y}{r}",font_size=30).move_to(big_black_background.get_center() + 0.35*DOWN)
        #the double brackets splits into subtext so I can call r_cosine_text[4] for \theta etc
        ##IMPORTANT NOTE: THE WHITE SPACES COUNT A INDICES OF THE SUBSTRING
        ##                          0  1    2   3      4    5   6   7  8
        r_cosine_text = MathTex(r"{{r}} {{cos(}} {{ \theta}} {{)= }} {{x}}",font_size=30).move_to(big_black_background.get_center() + 0.35*UP)
        r_sine_text = MathTex(r"{{r}} {{sin(}} {{\theta}} {{)= }} {{y}}",font_size=30).move_to(big_black_background.get_center() + 0.35*DOWN)
        radius_label = MathTex(r"{{r}} {{=2}}",font_size=32)

      
        #initiate updaters
        dynamic_cosine_text = MathTex()
        dynamic_sine_text = MathTex()
        dynamic_ordered_pair_text = MathTex()
        cosine_graph_dot = Dot()
        sine_graph_dot = Dot()

        #all updaters

        #for the red line
        line_moving.add_updater(
            lambda x: x.become(line_ref.copy().set_color(RED)).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            ).set_z_index(1)
        )

        #for the angle
        a.add_updater(
            lambda x: x.become(Angle(line1, line_moving, radius=0.25, other_angle=False))
        )
        #for the symbol theta
        tex.add_updater(
            lambda x: x.move_to(
                Angle(
                    line1, line_moving, radius=0.35 + 3 * SMALL_BUFF, other_angle=False
                ).point_from_proportion(0.5)
            )
        )
        #line that is projected up/down onto the x axis
        x_proj_line.add_updater(
            lambda x: x.become(Line(axes.coords_to_point(2*np.cos(theta_tracker.get_value()*DEGREES), 0), axes.coords_to_point(2*np.cos(theta_tracker.get_value()*DEGREES), 2*np.sin(theta_tracker.get_value()*DEGREES)))
        ).set_color(YELLOW)
        )
        #length of that projection
        x_proj_length.add_updater(
            lambda x: x.become(Line(axes.coords_to_point(0, 0), axes.coords_to_point(2*np.cos(theta_tracker.get_value()*DEGREES), 0))
        ).set_color(GREEN)
        )
        #line that is projected left/right onto the y axis
        y_proj_line.add_updater(
            lambda x: x.become(Line(axes.coords_to_point(0,2*np.sin(theta_tracker.get_value()*DEGREES)), axes.coords_to_point(2*np.cos(theta_tracker.get_value()*DEGREES), 2*np.sin(theta_tracker.get_value()*DEGREES)))
        ).set_color(GREEN)
        )
        #length of that projection
        y_proj_length.add_updater(
            lambda x: x.become(Line(axes.coords_to_point(0, 0), axes.coords_to_point(0,2*np.sin(theta_tracker.get_value()*DEGREES)))
        ).set_color(YELLOW)
        )



        #changing cosine text equation, it is shifted 0.0004 to avoid -0.00 because I was getting -1E-16 for cos(270) (bc pi infinitely long)
        dynamic_cosine_text.add_updater(
            lambda x: x.become(MathTex(r"{{2}} {{\cos(}}" + 
                                       "{:.2f}".format(theta_tracker.get_value()) + 
                                       r"{{)=}}" +
                                       "{:.2f}".format(2*np.cos(theta_tracker.get_value()*DEGREES) +0.0004),font_size=30
                                        ).move_to(r_cosine_text.get_center())
                                        )
        )

        #set colors for dynamic cosine text, the indices come from the double bracket notation {{ }}
        dynamic_cosine_text.add_updater(
            lambda x: x[0].set_color(RED)
        )
        dynamic_cosine_text.add_updater(
            lambda x: x[5].set_color(GREEN)
        )

        #creates dynamic sine text equation, and sets color and position
        dynamic_sine_text.add_updater(
            lambda x: x.become(MathTex(r"{{2}} {{\sin(}}" +
                                       "{:.2f}".format(theta_tracker.get_value()) +
                                       r"{{)=}}" +
                                       "{:.2f}".format(2*np.sin(theta_tracker.get_value()*DEGREES)),font_size=30
                                       ).move_to(r_sine_text.get_center())
                                       )
        )
        #sets color for dynamic sine text
        dynamic_sine_text.add_updater(
            lambda x: x[0].set_color(RED)
        )
        dynamic_sine_text.add_updater(
            lambda x: x[5].set_color(YELLOW)
        )

        #dot that moves along the graph of x vs theta
        cosine_graph_dot.add_updater(
            lambda x: x.become(Dot(point=[cosine_sub_axes.coords_to_point(theta_tracker.get_value(),2*np.cos(theta_tracker.get_value()*DEGREES))],color=TEAL)
                               ))
        
        #dot that moves along the graph of y vs theta
        sine_graph_dot.add_updater(
            lambda x: x.become(Dot(point=[sine_sub_axes.coords_to_point(theta_tracker.get_value(),2*np.sin(theta_tracker.get_value()*DEGREES))],color=TEAL)
                               ))      

        #Dot that is the ordered pair on circle of radius 2
        ordered_pair.add_updater(
            lambda x: x.become(Dot(point=[2*np.cos(theta_tracker.get_value()*DEGREES), 2*np.sin(theta_tracker.get_value()*DEGREES), 0],color=TEAL)).set_z_index(5)
        )

        #ordered pair updating text and background
        dynamic_ordered_pair_text.add_updater(
            lambda x: x.become(MathTex(r"{{(}}" +
                                       "{:.2f}".format(2*np.cos(theta_tracker.get_value()*DEGREES) + 0.0004) +
                                       r"{{,}}" +
                                       "{:.2f}".format(2*np.sin(theta_tracker.get_value()*DEGREES)) +
                                       r"{{)}}", font_size=28
                                       )).move_to([3*np.cos(theta_tracker.get_value()*DEGREES), 3*np.sin(theta_tracker.get_value()*DEGREES), 0]).set_z_index(4)
        )

        #set color of x and y for ordered pair
        dynamic_ordered_pair_text.add_updater(
            lambda x: x[1].set_color(GREEN)
        )
        dynamic_ordered_pair_text.add_updater(
            lambda x: x[3].set_color(YELLOW)
        )
        
        #background for the ordered pair
        ordered_pair_background.add_updater(
            lambda x: x.move_to([3*np.cos(theta_tracker.get_value()*DEGREES), 3*np.sin(theta_tracker.get_value()*DEGREES), 0]).set_z_index(3)
        )


        #groups for sine and cosine for graphs and for the circle projections and equations
        cosine_graph = cosine_sub_axes.plot(lambda x: 2*np.cos(x*DEGREES), x_range=[0,720]).set_color(GREEN)
        sine_graph = sine_sub_axes.plot(lambda x: 2*np.sin(x*DEGREES), x_range=[0,720]).set_color(YELLOW)

        cosine_group=VGroup()
        cosine_group.add(dynamic_cosine_text,x_proj_length,x_proj_line)

        sine_group=VGroup()
        sine_group.add(dynamic_sine_text,y_proj_length,y_proj_line)

        cosine_graph_group=VGroup()
        cosine_graph_group.add(cosine_sub_axes, cosine_sub_axes_labels ,cosine_graph, cosine_graph_dot)

        sine_graph_group=VGroup()
        sine_graph_group.add(sine_sub_axes, sine_sub_axes_labels, sine_graph, sine_graph_dot)

        ordered_pair_group = VGroup()
        ordered_pair_group.add(ordered_pair,dynamic_ordered_pair_text,ordered_pair_background)

        

        #######################################################################################
        #function for inspection all crucial ordered pairs (pairs on the axis)

        
        #begin video with two lines rotating
        ##NOTE ALL self.wait(x) times are by my choice, because I am overlaying audio, and want to time movements based on my speech.
        self.play(Succession(
            Write(line1),
            Write(line_moving),
            Write(a),
            Write(tex)
        )
        ) 

        #cycle_through_quadrants(my_run_time=0.5, my_rate_func=smooth, my_wait_time=0.5)
        rotate_to_quadrant("II", my_run_time=1,my_wait_time=1,eliminate_near_crucial=True)
        rotate_to_quadrant("IV",my_run_time=1,my_wait_time=1,eliminate_near_crucial=True)
        rotate_to_quadrant("I",my_run_time=1,my_wait_time=1,eliminate_near_crucial=True)
        line1.save_state()

        #draw circle, perform rotation, and transforms
        self.play(Create(circle))
        rotate_to_quadrant("IV",my_run_time=1,my_wait_time=1,eliminate_near_crucial=True)
        self.play(Transform(line1, Line(axes.coords_to_point(0,0),axes.coords_to_point(1,0))))
        self.wait(4)
        circle.save_state()
        self.play(Unwrite(circle), Restore(line1), theta_tracker.animate.set_value(45))

        #overlay axes with labels, create circle of radius 2, add equations
        self.play(Write(axes), Write(labels))
        self.wait(2)
        circle.restore()
        self.play(Create(circle))
        self.wait(4)
        self.play(Unwrite(labels), Write(big_black_background))
        self.play(Write(cosine_text), Write(sine_text))
        self.wait(4)

        #set static equation colors and transform to r_ equations
        set_static_equation_colors(r_cosine_text,r_sine_text,0,8)
        self.play(Transform(cosine_text, r_cosine_text), Transform(sine_text, r_sine_text))
        
        
        #setup for r=2 label above line moving for a random theta in the first quadrant (my choice)
        radius_label.move_to(line_moving.get_center()+[-0.25*np.cos(theta_tracker.get_value()*DEGREES),0.25*np.sin(theta_tracker.get_value()*DEGREES),0] , aligned_edge=DOWN).set_color(RED).rotate(theta_tracker.get_value()*DEGREES)
        self.play(Write(radius_label))

        #move r and /theta from the circle to the equations
        save_state_and_transform(copied_mobject=radius_label, transform_to=r_cosine_text, i=0, j=0, is_substring=True)
        save_state_and_transform(copied_mobject=tex, transform_to=r_cosine_text,j=4)
        save_state_and_transform(copied_mobject=radius_label, transform_to=r_sine_text, i=0, j=0, is_substring=True)
        save_state_and_transform(copied_mobject=tex, transform_to=r_sine_text,j=4)

        #save state of r_cosine and r_sine so we know where to position dynamic_cosine and dynamic_sine, and Unwrite the static equations
        r_cosine_text.save_state()
        r_sine_text.save_state()
        self.play(Unwrite(radius_label), Unwrite(r_cosine_text), Unwrite(r_sine_text), Unwrite(cosine_text), Unwrite(sine_text))
        self.wait(2)

        #show cosine equation and plot x vs theta, then rotate
        self.play(Write(dynamic_cosine_text))
        self.wait(2)
        self.play(Write(left_big_black_background))
        self.play(Write(cosine_graph_group))
        rotate_to_quadrant(quadrant_numeral="II",eliminate_near_crucial=True)

        #adjust z index and write
        set_pair_mobj_z_index(x_proj_length,x_proj_line,3)
        self.play(Write(x_proj_line),Write(x_proj_length))
   

        #show arrow that shows length along y
        self.wait(8)
        self.play(Write(length_arrow))
        self.play(length_arrow.animate.move_to([2*np.cos(theta_tracker.get_value()*DEGREES),-0.75,0]),run_time=4,rate_func=linear)
        self.play(Unwrite(length_arrow))
        self.wait(2)

        ##LOOKING AT ORDERED PAIRS
        self.play(Write(ordered_pair),Write(dynamic_ordered_pair_text),Write(ordered_pair_background))
        self.wait(4)
        cycle_through_quadrants()

        #loop through ordered pairs when they are on the axes
        inspect_crucial_points()

        #choose these specific values because the numbers come out clean for cosine
        self.play(theta_tracker.animate.set_value(245),rate_func=linear)
        self.wait(4)
        self.play(theta_tracker.animate.set_value(120),rate_func=linear,run_time=3)
        self.wait(4)

        #save cosine group state and remove so I can rewrite the cosine group later
        cosine_graph_group.save_state()
        self.remove(dynamic_cosine_text,x_proj_length,x_proj_line)
        self.play(Unwrite(cosine_graph_group))
        self.wait(4)


        #THIS PART SHOWS SINE

        #bring sine projections in front of cosine projections, and rotate
        set_pair_mobj_z_index(y_proj_length,y_proj_line,4)
        self.play(Write(dynamic_sine_text),Write(sine_graph_group))
        self.wait(4)
        self.play(Write(y_proj_line), Write(y_proj_length))
        self.wait(4)
        rotate_to_quadrant("I",my_run_time=1,my_wait_time=1, eliminate_near_crucial=True)
        self.wait(4)
        
        #show arrow that shows length along y here
        self.play(Write(y_length_arrow))
        self.play(y_length_arrow.animate.move_to([-0.75,2*np.sin(theta_tracker.get_value()*DEGREES),0]),run_time=4,rate_func=linear)
        self.play(Unwrite(y_length_arrow))

        #choose a random theta in each quadrant
        cycle_through_quadrants()

        #loop through ordered pairs when they are on the axes
        inspect_crucial_points()

        #Introduce both sine and cosine together
        cosine_graph_group.restore()
        self.play(Write(cosine_group))
        self.play(Write(cosine_graph_group))
        self.wait(4)

        #choose a random theta in each quadrant, slower rotations
        cycle_through_quadrants()

        #loop through a full rotation twice
        cycle_full_rotation()
        cycle_full_rotation()
        ##END


