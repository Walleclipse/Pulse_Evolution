# Pulse Evolution
## Python modeling for ultrafast optics and supercontinuum generation
<img src="https://github.com/Walleclipse/Pulse_Evolution/blob/master/source/img/logo.gif" width=500 >

This project provides a very easy way to simulate pulse evolution fibers. It provides many functionalities for representing pulses of lasers, fibers, and methods for simulating four-wave-mixing processes such as supercontinuum generation as well as functions for calculating beta and gamma parameter in fibers. Also, It provides a simple and easy-to-use GUI.

## How to use it
There are two ways to run the project.

1 . Run executable file.
  * Download executable file from [here](https://pan.baidu.com/s/1rPRhpnJGCR_TN4qjVO2qDA)
  * Run `pulse_evolution.exe`

2 . Run Python file.
  * `git clone https://github.com/Walleclipse/Pulse_Evolution.git`
  * `pip install -r requirements.txt`
  *  `python main.py`

The GUI is as follows:

<img src="https://github.com/Walleclipse/Pulse_Evolution/blob/master/source/img/ui.png"  width=600>

After setting the parameter of the pulse, fiber and propagation, click the `Run` bottom.  

The sample result is as follows (the blue curve represents input pulse, the red curve represents output pulse): 

<img src="https://github.com/Walleclipse/Pulse_Evolution/blob/master/source/img/result.png"  width=600>

Also, this project provides simple functions for calculating beta_n and gamma parameters for pulse evolution in fiber.

<table><tr>
<td><img src="https://github.com/Walleclipse/Pulse_Evolution/blob/master/source/img/epp.png" border=0></td>
<td><img src="https://github.com/Walleclipse/Pulse_Evolution/blob/master/source/img/beta.png" border=0></td>
</tr></table>

<img src="https://github.com/Walleclipse/Pulse_Evolution/blob/master/source/img/gamma.png"  width=300>



