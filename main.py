import tkinter as tk
from functools import partial
from tkinter import ttk

from source import PulseEvolution


def create_combobox(window, label, var, x, y):
	tk.Label(window, text=label).place(x=x, y=y)  # 创建一个`label`名为`User name: `置于坐标（50,150）
	cmb = ttk.Combobox(window)
	cmb['value'] = var
	cmb.current(0)
	cmb.place(x=x + 150, y=y)
	return cmb


def create_entry(window, label, var, x, y):
	tk.Label(window, text=label).place(x=x, y=y)  # 创建一个`label`名为`User name: `置于坐标（50,150）
	item_var = tk.StringVar()
	item_var.set(str(var))
	item_entry = tk.Entry(window, textvariable=item_var)
	item_entry.place(x=x + 150, y=y)
	return item_entry


def run(params):
	# pulse
	pulse_shape = params['pulse'].get()
	frep_MHz =  eval(params['frep'].get())
	FWHM_ps =  eval(params['fwhm'].get())
	center_wavelength_nm =  eval(params['wl'].get())
	EPP_nj =  eval(params['epp'].get())
	GDD = eval(params['gdd'].get())
	TOD =  eval(params['tod'].get())
	time_window_ps =  eval(params['window'].get())
	NPTS =  eval(params['npts'].get())
	# fiber
	fiber_from = params['fiber'].get()
	length_mm = eval(params['ln'].get())
	fibel_cl = eval(params['fibel_cl'].get())
	alpha_db_cm = eval(params['alpha'].get())
	beta2 =  eval(params['beta2'].get())
	beta3 =  eval(params['beta3'].get())
	beta4 =  eval(params['beta4'].get())
	gamma_W_m =  eval(params['gamma'].get())
	pitch_um =  eval(params['pitch'].get())
	duty_ratio = eval(params['dr'].get())
	# propogate
	n_steps =   eval(params['steps'].get())
	Raman =  eval(params['raman'].get())
	self_steepening =  eval(params['steep'].get())

	solver = PulseEvolution()
	solver.init_pulse(pulse_shape=pulse_shape, frep_MHz=frep_MHz, FWHM_ps=FWHM_ps,
	                  center_wavelength_nm=center_wavelength_nm,
	                  EPP_nj=EPP_nj, time_window_ps=time_window_ps, GDD=GDD, TOD=TOD,
	                  NPTS=NPTS)
	if fiber_from=='pitch':
		solver.init_fiber(length_mm=length_mm, center_wavelength_nm=fibel_cl, pitch_um=pitch_um,
		                  duty_ratio=duty_ratio,
		                  alpha_db_cm=alpha_db_cm, use_pitch=True)
	else:
		solver.init_fiber(length_mm=length_mm, center_wavelength_nm=fibel_cl, betas=(beta2, beta3, beta4),
	                  gamma_W_m=gamma_W_m, alpha_db_cm=alpha_db_cm, use_pitch=False)

	solver.propogation(n_steps=n_steps, Raman=Raman, self_steepening=self_steepening)


def main():
	window = tk.Tk()
	window.title('Pulse Evolution')
	window.geometry('800x650')
	base_x = 50
	base_y=110
	p_base_x = 450
	params = {}
	# welcome
	canvas = tk.Canvas(window, height=100, width=700)  # 创建画布
	image_file = tk.PhotoImage(file='source/img/gui.gif')  # 加载图片文件
	canvas.create_image(0, 0, anchor='nw', image=image_file)
	canvas.pack(side='top')
	# pulse params
	tk.Label(window, text='Pulse Parameter', fg='blue', font=('Arial', 12)).place(x=350, y=base_y)
	params['pulse'] = create_combobox(window, 'Pulse Shape', ('sech', 'gaussian', 'sinc'), base_x, base_y+30)
	params['frep'] = create_entry(window, 'Frep [MHz]', 100, p_base_x,  base_y+30)
	params['fwhm'] = create_entry(window, 'FWHM [ps]', 0.050, base_x,  base_y+60)
	params['wl'] = create_entry(window, 'Center Wavelength [nm]', 1550, p_base_x,  base_y+60)
	params['epp'] = create_entry(window, 'EPP [nj]', 0.1, base_x, base_y+90)
	params['gdd'] = create_entry(window, 'GDD [ps^2]', 0, p_base_x, base_y+90)
	params['tod'] = create_entry(window, 'TOD [ps^3]', 0, base_x, base_y+120)
	params['window'] = create_entry(window, 'Time Window [ps]', 10, p_base_x, base_y+120)
	params['npts'] = create_entry(window, 'Number of Points', 2 ** 13, base_x, base_y+150)
	# fiber params
	tk.Label(window, text='Fiber Parameter', fg='blue', font=('Arial', 12)).place(x=350, y=base_y+190)
	params['fiber'] = create_combobox(window, 'Create fiber from', ('beta', 'pitch'), base_x, base_y+220)
	params['ln'] = create_entry(window, 'Length [mm]', 20, p_base_x, base_y+220)
	params['fibel_cl'] = create_entry(window, 'Center Wavelength [nm]', 1550, base_x, base_y+250)
	params['alpha'] = create_entry(window, 'alpha [dB/cm]', 0.0, p_base_x, base_y+250)
	params['beta2'] = create_entry(window, 'beta2 [ps^2/km]', -120.0, base_x, base_y+280)
	params['beta3'] = create_entry(window, 'beta3 [ps^3/km]', 0.00, p_base_x, base_y+280)
	params['beta4'] = create_entry(window, 'beta4 [ps^4/km]', 0.005, base_x, base_y+310)
	params['gamma'] = create_entry(window, 'gamma [1/(W·m)]', 1.0, p_base_x, base_y+310)
	params['dr'] = create_entry(window, 'Duty Ratio (optional)', 0.53, base_x, base_y+340)
	params['pitch'] = create_entry(window, 'Pitch [um] (optional)', (3.1, 3.0, 2.9), p_base_x, base_y+340)
	# propogate params
	tk.Label(window, text='Propagation Parameter', fg='blue', font=('Arial', 12)).place(x=350, y=base_y+380)
	params['raman'] = create_combobox(window, 'Raman', ('True', 'False'), base_x, base_y+410)
	params['steep'] = create_combobox(window, 'Self Steeping', ('True', 'False'), p_base_x, base_y+410)
	params['steps'] = create_entry(window, 'Number of Steps', 100, base_x, base_y+440)

	#run
	btn = tk.Button(window, text='Run',bg='LightCyan',activebackground='DeepSkyBlue',
	                font=('Arial', 16),fg='red',
	                command=partial(run, params=params))
	btn.place(x=370, y=base_y+480)

	window.mainloop()

main()
