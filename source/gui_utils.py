from .pulse_evolution import PulseEvolution
import tkinter as tk

from functools import partial
from tkinter import ttk,messagebox


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
	try:
		pulse_shape = params['pulse'].get()
		frep_MHz =  eval(params['frep'].get())
		FWHM_ps =  eval(params['fwhm'].get())
		center_wavelength_nm =  eval(params['wl'].get())
		EPP_nj =  eval(params['epp'].get())
		GDD = eval(params['gdd'].get())
		TOD =  eval(params['tod'].get())
		time_window_ps =  eval(params['window'].get())
		NPTS =  eval(params['npts'].get())
	except:
		msg = 'Pulse Parameter Error! Please check the format of pulse parameters'
		messagebox.showerror(title='Pulse Parameter Error', message=msg)
		raise (msg)
	# fiber
	try:
		length_mm = eval(params['ln'].get())
		fibel_cl = eval(params['fibel_cl'].get())
		alpha_db_cm = eval(params['alpha'].get())
		beta2 = eval(params['beta2'].get())
		beta3 = eval(params['beta3'].get())
		beta4 = eval(params['beta4'].get())
		gamma_W_m =  eval(params['gamma'].get())
	except:
		msg = 'Fiber Parameter Error! Please check the format of fiber parameters'
		messagebox.showerror(title='Fiber Parameter Error', message=msg)
		raise (msg)
	# propogate
	try:
		n_steps =  eval(params['steps'].get())
		Raman =  eval(params['raman'].get())
		self_steepening =  eval(params['steep'].get())
	except:
		msg = 'Propagation Parameter Error! Please check the format of propagation parameters'
		messagebox.showerror(title='Propagation Parameter Error', message=msg)
		raise (msg)

	if isinstance(beta2, int) or isinstance(beta2, float):
		beta2 = (beta2,)
	if isinstance(beta3, int) or isinstance(beta3, float):
		beta3 = (beta3,)
	if isinstance(beta4, int) or isinstance(beta4, float):
		beta4 = (beta4,)
	if isinstance(gamma_W_m, int) or isinstance(gamma_W_m, float):
		gamma_W_m = (gamma_W_m,)

	solver = PulseEvolution()
	try:
		solver.init_pulse(pulse_shape=pulse_shape, frep_MHz=frep_MHz, FWHM_ps=FWHM_ps,
	                  center_wavelength_nm=center_wavelength_nm,
	                  EPP_nj=EPP_nj, time_window_ps=time_window_ps, GDD=GDD, TOD=TOD,
	                  NPTS=NPTS)
	except:
		msg = 'Pulse Parameter Error! Please check the format of pulse parameters'
		messagebox.showerror(title='Pulse Parameter Error', message=msg)
		raise (msg)

	try:
		solver.init_fiber(length_mm=length_mm, center_wavelength_nm=fibel_cl,
	                  beta_2=beta2, beta_3=beta3, beta_4=beta4, gamma_W_m=gamma_W_m,
		                  alpha_db_cm=alpha_db_cm, )
	except:
		msg = 'Fiber Parameter Error! Please check the format of fiber parameters'
		messagebox.showerror(title='Fiber Parameter Error', message=msg)
		raise (msg)
	try:
		solver.propogation(n_steps=n_steps, Raman=Raman, self_steepening=self_steepening)
	except:
		msg = 'Parameter Error! Please check the format of parameters'
		messagebox.showerror(title='Parameter Error', message=msg)
		raise (msg)

def _cal_epp(params,params_2,window_2):
	try:
		frep_MHz = eval(params_2['frep'].get())
		power = eval(params_2['power'].get())
		solver = PulseEvolution()
		epp = solver.cal_epp(power=power,frep_MHz=frep_MHz)
		msg = "Calculated EPP = {} [nj]".format(epp)
		messagebox.showinfo(title='EPP', message=msg)
		params['epp'].delete(0, 'end')
		params['epp'].insert(0,str(epp))
		window_2.destroy()
	except:
		msg = 'Calculate EPP Parameter Error! Please check the format of calculate_EPP parameters'
		messagebox.showerror(title='Calculate EPP Parameter Error', message=msg)
		raise (msg)

def get_epp(params,window):
	window_2 = tk.Toplevel(window)
	window_2.geometry('320x110')
	window_2.title('Calculate EPP')
	params_2={}
	params_2['frep'] = create_entry(window_2, 'Frep [MHz]', 100, 10, 10)
	params_2['power'] = create_entry(window_2, 'Average power [mW]', 10, 10, 40)

	btn = tk.Button(window_2, text='Calculate EPP',bg='LightCyan',
	                font=('Arial', 10),
	                command=partial(_cal_epp, params=params,params_2=params_2,window_2=window_2))
	btn.place(x=120, y=70)

def _cal_beta(params,params_2,window_2):
	try:
		duty = eval(params_2['duty'].get())
		pitch = eval(params_2['pitch'].get())
		center_wl = eval(params_2['center_wl'].get())

		solver = PulseEvolution()
		if isinstance(pitch,int) or isinstance(pitch,float):
			pitch = (pitch,)
		beta_2, beta_3, beta_4, gamma = solver.cal_fiber_parameter(duty_ratio=duty,pitch_um=pitch, center_wl=center_wl)
		msg = 'Calculated beta_n:\n'
		for ii in range(len(beta_2)):
			temp='for fiber{}: beta_2 = {} [ps^2/m], beta_3 = {} [ps^3/m], beta_4 = {} [ps^4/m]\n'.format(ii+1,beta_2[ii],beta_3[ii],beta_4[ii])
			msg += temp

		if len(beta_2)==1:
			beta_2 = beta_2[0]
		if len(beta_3)==1:
			beta_3 = beta_3[0]
		if len(beta_4)==1:
			beta_4 = beta_4[0]

		messagebox.showinfo(title='beta_n', message=msg)
		params['beta2'].delete(0, 'end')
		params['beta2'].insert(0,str(beta_2))
		params['beta3'].delete(0, 'end')
		params['beta3'].insert(0,str(beta_3))
		params['beta4'].delete(0, 'end')
		params['beta4'].insert(0,str(beta_4))
		window_2.destroy()
	except:
		msg = 'Calculated beta_n Parameter Error! Please check the format of calculate_beta_n parameters'
		messagebox.showerror(title='Calculate beta_n Parameter Error', message=msg)
		raise (msg)

def get_beta(params,window):
	window_2 = tk.Toplevel(window)
	window_2.geometry('320x140')
	window_2.title('Calculate beta_n')
	params_2={}
	params_2['duty'] = create_entry(window_2, 'Duty Ratio', 0.53, 10, 10)
	params_2['pitch'] = create_entry(window_2, 'Pitch [um]', (3.1, 2.9), 10, 40)
	params_2['center_wl'] = create_entry(window_2, 'Pulse Center Wavelength [nm]', 1550, 10, 70)

	btn = tk.Button(window_2, text='Calculate beta_n for PCF',bg='LightCyan',
	                font=('Arial', 10),
	                command=partial(_cal_beta, params=params,params_2=params_2,window_2=window_2))
	btn.place(x=80, y=100)


def _cal_gamma(params, params_2, window_2):
	try:
		duty = eval(params_2['duty'].get())
		pitch = eval(params_2['pitch'].get())
		center_wl = eval(params_2['center_wl'].get())

		solver = PulseEvolution()
		if isinstance(pitch, int) or isinstance(pitch, float):
			pitch = (pitch,)
		beta_2, beta_3, beta_4, gamma = solver.cal_fiber_parameter(duty_ratio=duty, pitch_um=pitch, center_wl=center_wl)
		msg = 'Calculated gamma:\n'
		for ii in range(len(gamma)):
			temp = 'for fiber{}: gamma = {} [1/(W·m)]\n'.format(ii+1, gamma[ii])
			msg += temp

		if len(gamma) == 1:
			gamma = gamma[0]

		messagebox.showinfo(title='gamma', message=msg)
		params['gamma'].delete(0, 'end')
		params['gamma'].insert(0, str(gamma))
		window_2.destroy()
	except:
		msg = 'Calculated gamma Parameter Error! Please check the format of calculate_gamma parameters'
		messagebox.showerror(title='Calculate gamma Parameter Error', message=msg)
		raise (msg)

def _cal_gamma_Aeff(params, params_2, window_2):
	try:
		area = eval(params_2['area'].get())
		center_wl = eval(params_2['center_wl'].get())

		solver = PulseEvolution()
		if isinstance(area, int) or isinstance(area, float):
			area = (area,)
		gamma = solver.cal_gamma_Aeff(Aeff=area, center_wl=center_wl)
		msg = 'Calculated gamma:\n'
		for ii in range(len(gamma)):
			temp = 'for fiber{}: gamma = {} [1/(W·m)]\n'.format(ii+1, gamma[ii])
			msg += temp

		if len(gamma) == 1:
			gamma = gamma[0]

		messagebox.showinfo(title='gamma', message=msg)
		params['gamma'].delete(0, 'end')
		params['gamma'].insert(0, str(gamma))
		window_2.destroy()
	except:
		msg = 'Calculated gamma Parameter Error! Please check the format of calculate_gamma_with_Aeff parameters'
		messagebox.showerror(title='Calculate gamma Parameter Error', message=msg)
		raise (msg)

def get_gamma(params, window):
	window_2 = tk.Toplevel(window)
	window_2.geometry('320x260')
	window_2.title('Calculate gamma')
	params_2 = {}
	params_2['duty'] = create_entry(window_2, 'Duty Ratio', 0.53, 10, 10)
	params_2['pitch'] = create_entry(window_2, 'Pitch [um]', (3.1, 2.9), 10, 40)
	params_2['center_wl'] = create_entry(window_2, 'Pulse Center Wavelength [nm]', 1550, 10, 70)

	btn = tk.Button(window_2, text='Calculate gamma for PCF', bg='LightCyan',
	                font=('Arial', 10),
	                command=partial(_cal_gamma, params=params, params_2=params_2, window_2=window_2))
	btn.place(x=80, y=100)

	params_2['area'] = create_entry(window_2, 'effective area [um^2]', 2.7939, 10, 160)
	params_2['center_wl_2'] = create_entry(window_2, 'Pulse Center Wavelength [nm]', 1550, 10, 190)

	btn = tk.Button(window_2, text='Calculate gamma from effective area', bg='LightCyan',
	                font=('Arial', 10),
	                command=partial(_cal_gamma_Aeff, params=params, params_2=params_2, window_2=window_2))
	btn.place(x=50, y=220)