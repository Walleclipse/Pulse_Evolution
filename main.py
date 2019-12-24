
import tkinter as tk
from functools import partial

from source import create_combobox, create_entry, run, get_epp, get_beta, get_gamma


def main():
	window = tk.Tk()
	window.title('Pulse Evolution')
	window.geometry('800x650')
	base_x = 50
	base_y=110
	p_base_x = 450
	params = {}
	# welcome
	canvas = tk.Canvas(window, height=100, width=700)
	image_file = tk.PhotoImage(file='source/img/logo.gif')
	canvas.create_image(0, 0, anchor='nw', image=image_file)
	canvas.pack(side='top')
	# pulse params
	tk.Label(window, text='Pulse Parameter', fg='blue', font=('Arial', 12)).place(x=350, y=base_y)
	params['pulse'] = create_combobox(window, 'Pulse Shape', ('sech', 'gaussian', 'sinc'), base_x, base_y+30)
	params['frep'] = create_entry(window, 'Frep [MHz]', 100, p_base_x,  base_y+30)
	params['fwhm'] = create_entry(window, 'FWHM [ps]', 0.050, base_x,  base_y+60)
	params['wl'] = create_entry(window, 'Center Wavelength [nm]', 1550, p_base_x,  base_y+60)
	params['gdd'] = create_entry(window, 'GDD [ps^2]', 0, base_x, base_y+90)
	params['tod'] = create_entry(window, 'TOD [ps^3]', 0, p_base_x, base_y+90)
	params['window'] = create_entry(window, 'Time Window [ps]', 10, base_x, base_y+120)
	params['npts'] = create_entry(window, 'Number of Points', 2 ** 13, p_base_x, base_y+120)
	params['epp'] = create_entry(window, 'EPP [nj]', 0.1, base_x, base_y+150)
	btn_epp = tk.Button(window, text='Calculate EPP',#bg='LightCyan',
	                font=('Arial', 9),
	                command=partial(get_epp, params=params,window=window))
	btn_epp.place(x=p_base_x-100, y=base_y+150)
	# fiber params
	tk.Label(window, text='Fiber Parameter', fg='blue', font=('Arial', 12)).place(x=350, y=base_y+190)
	params['ln'] = create_entry(window, 'Length [mm]', 20, base_x, base_y+220)
	params['fibel_cl'] = create_entry(window, 'Center Wavelength [nm]', 1550, p_base_x, base_y+220)
	params['alpha'] = create_entry(window, 'alpha [dB/cm]', 0.0, base_x, base_y + 250)
	params['beta2'] = create_entry(window, 'beta2 [ps^2/m]', -0.12, base_x, base_y+280)
	params['beta3'] = create_entry(window, 'beta3 [ps^3/m]', 0.00, p_base_x, base_y+280)
	params['beta4'] = create_entry(window, 'beta4 [ps^4/m]', 0.000005, base_x, base_y+310)
	btn_beta= tk.Button(window, text='Calculate beta_n',#bg='LightCyan',
	                font=('Arial', 9),
	                command=partial(get_beta, params=params,window=window))
	btn_beta.place(x=p_base_x-100, y=base_y+310)

	params['gamma'] = create_entry(window, 'gamma [1/(W·m)]', 1.0, base_x, base_y+340)
	btn_gamma= tk.Button(window, text='Calculate gamma',#bg='LightCyan',
	                font=('Arial', 9),
	                command=partial(get_gamma, params=params,window=window))
	btn_gamma.place(x=p_base_x-100, y=base_y+340)
	# propogate params
	tk.Label(window, text='Propagation Parameter', fg='blue', font=('Arial', 12)).place(x=350, y=base_y+380)
	params['raman'] = create_combobox(window, 'Raman', ('True', 'False'), base_x, base_y+410)
	params['steep'] = create_combobox(window, 'Self Steeping', ('True', 'False'), p_base_x, base_y+410)
	params['steps'] = create_entry(window, 'Number of Steps', 100, base_x, base_y+440)

	#run
	btn_run = tk.Button(window, text='Run',bg='LightCyan',activebackground='DeepSkyBlue',
	                font=('Arial', 16),fg='red',
	                command=partial(run, params=params))
	btn_run.place(x=370, y=base_y+480)

	window.mainloop()

main()
