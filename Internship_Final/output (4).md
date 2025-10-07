Supervisor:	

	Dr . LYDIA  , M.E , Ph.D , 
	Professor ,
	  Mechatronics Engineering         

Department of Mechatronics Engineering
23MT507- Prototype Lab
First Review
Date : 09-08-2025





Design and Fabrication of IoT Controlled Two Wheeled Self Balancing Robot 
Team Members :
	727723EUMT011 - AKASH K 	
	727723EUMT050 - HARISH S
	727723EUMT058 - KALAISELVAN M
	727723EUMT061 - KANNAN S	

                                                  
                                                            

PROBLEM STATEMENT
 The adoption of self-balancing robotic platforms in education is limited by the lack of simple, affordable, and adaptable designs that can be easily implemented by students.

 The absence of accessible, non-PID-based control approaches and open learning resources restricts opportunities for learners to explore balance control, sensor integration, and embedded programming in a hands-on manner.

 This gap in practical, low-cost, and beginner-friendly robotics solutions hinders students from developing essential skills in real-time control systems, mechatronics, and applied electronics.
OBJECTIVE
 Design and prototype a two-wheeled, IoT-controlled self-balancing robot with stable upright posture control for diverse future developments

LITERATURE REVIEW
GANTT CHART





BLOCK DIAGRAM
PROJECT MODEL
TOP VIEW
FRONT VIEW
SIDE VIEW
DESIGN CALCULATION
Dimensions :
		Mass (m) : 250 g = 0.25 kg
	Height     : 100 mm (0.10 m)
  		Length    : 80 mm (0.08 m)
Breadth   : 65 mm (0.065 m)

Wheel Diameter Calculation: 

		Total no. of wheels, n= 2
		Weight exerted per wheel, W = m/n
					 = 0.25/2 
					 = 0.125 Kg
Wheel Selection: 
		 Wheel Thickness = 25 mm (0.025 m)
		 The selected wheel is a 60 mm rubber wheel,  and it has the ability to withstand our robot’s weight.

Motor calculation: 

		Torque & power required must be calculated Speed of AMR = 0.5m/s

		Speed in m/s  = 0.5 m/s
		Velocity in m/s = 0.5 m/s
 		Speed with respect to rpm: N = (v x 60)/(π x D) 
			        		= (0.5 x 60) / (πx 0.06) 							= 159.15 rpm			
					= 160 rpm (for 2 motors)
Torque Required:

		T = F x r 
		Here,
		 F = w x g  (F = m x a) 
		w = 0.125 Kg  (for 1 wheel) 	and      g  = 9.81 m/s^2  (acceleration due to gravity) 
		F  = 0.125 x 9.81 N 
		    = 1.23 N 
		  T =  1.23 x 0.03  (Wheel radius in m) 
		  T = 0.037 Nm ( This Torque is for One Wheel ) . 
So, for Two Wheels , T Total = 2 x 0.037 = 0.074Nm

Power Required:


		P = w x T 
		Here, w = Angular Velocity 
		w = v/R 
		w = 0.5 / 0.03 
		    = 16.67 rad/s 
		P Total  = 16.67 x 0.037 
		           =  0.62 Watts (for 2 wheels) 
		Power required for one Wheel , P = 0.62 / 2
					        = 0.31 Watts

	 So , for the required calculations SPG30E-60K BO Geared Motor is Chosen
PROTOTYPE ITEMS PURCHASED
Gonzalez, C., Alvarado, I., & Peña, D. M. (2017). Low cost Two wheels self-balancing robot for control education. IFAC-PapersOnLine , 50(1). Low cost two-wheels self-balancing robot for control education – ScienceDirect

Ghanta Sai Krishna; Dyavat Sumith; Garika Akshay Epersist: A Two-Wheeled Self Balancing Robot Using PID Controller And Deep Reinforcement Learning . https://ieeexplore.ieee.org/document/10003940

AMCI Tech Tutorials. 2015. Stepper vs. Servo. Available at: http://www.amci.com/tutorials/tutorials-stepper-vs-servo.asp. [Accessed 13 May 2015].

Arduino Uno. 2015. Arduino - ArduinoBoardUno . Available at: http://www.arduino.cc/en/main/arduinoBoardUno. [Accessed 22 April 2015]

MathWorks Nordic. 2015. MATLAB - The Language of Technical Computing. Available at: http://se.mathworks.com/products/matlab/. [Accessed 21 April2015]




REFERENCES
THANKING YOU