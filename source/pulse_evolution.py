import os
import math
import numpy as np
from scipy import constants
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pynlo

class PulseEvolution(object):

	def __init__(self):
		self._c_m_s = constants.value('speed of light in vacuum')
		self._c_um_s = self._c_m_s * 1e6
		self._c_um_ps = self._c_um_s * 1e-12
		self._c_m_ps = self._c_m_s * 1e-12

	def _check_pitch(self,pitch_um,duty_ratio):
		duty_ratio=round(duty_ratio,2)

		valid_dr=[0.53,0.9]
		if duty_ratio not in valid_dr:
			raise ('Invalid duty_ratio! only accept duty_ratio = 0.53 or 0.9')
		if duty_ratio==0.53:
			for pitch in pitch_um:
				if pitch<1.4 or pitch>3.1:
					raise ('Invalid pitch_um! When duty_ratio=0.53, only accept 1.4 <= pitch_um <= 3.1')
		if duty_ratio==0.9:
			for pitch in pitch_um:
				if pitch<1.3 or pitch>7.0:
					raise ('Invalid pitch_um! When duty_ratio=0.9, only accept 1.3 <= pitch_um <= 7.0')

		return pitch_um,duty_ratio

	def _load_fiber_parameter(self,duty_ratio,pitch_LB, center_wl,beta_degree=14):
		with open('./source/d_p_0%d/dp%0.2f_p%0.1f.txt' % (duty_ratio * 100, duty_ratio, pitch_LB), 'r') as f:
			params = f.readlines()
		params = [x.strip().split() for x in params]
		params = np.array(params, dtype=np.float)

		wl = params[:,0] # um
		neff = params[:,1]
		area = params[:,3] #um^2

		omiga = 2 * np.pi * self._c_um_ps / wl   # /ps
		beta = neff * omiga / self._c_m_ps #  /m

		center_wl_um=center_wl/1000 #um
		omiga0 = 2 * np.pi * self._c_um_ps / center_wl_um
		coeff = np.polyfit(omiga - omiga0, beta, beta_degree)
		fact = np.zeros((beta_degree+1,))
		for ii in range(beta_degree+1):
			fact[ii]=math.factorial(ii)

		beta_n = coeff[-2::-1]*fact[1:]

		interpolator = interp1d(wl,area)
		area0 = interpolator([center_wl_um])[0]

		n2 = 2.6e-20 # nonlinear refractive index [m^2/W]
		area0 = area0 * 1e-12 # m^2
		gamma = n2 * (1e12*omiga0) / self._c_m_s / area0

		return beta_n, gamma

	def _dB(self,num):
		return 10 * np.log10(np.abs(num) ** 2)

	def cal_epp(self,power,frep_MHz):
		epp = 1e9 * power * 1.0e-3 / (frep_MHz * 1.0e6)
		return epp

	def cal_fiber_parameter(self,duty_ratio,pitch_um, center_wl,beta_degree=14):
		pitch_um, duty_ratio = self._check_pitch(pitch_um, duty_ratio)
		beta_2, beta_3, beta_4, gamma=[],[],[],[]
		for now_pitch in pitch_um:
			pitch_LB = math.floor(now_pitch * 10) / 10
			pitch_UB = pitch_LB + 0.1
			if (duty_ratio == 0.53 and pitch_UB == 1.4) or (duty_ratio == 0.9 and pitch_UB == 1.3):
				pitch_LB = pitch_UB

			b_LB, g0_LB = self._load_fiber_parameter(duty_ratio, pitch_LB, center_wl, beta_degree)
			if (duty_ratio == 0.53 and pitch_LB == 3.1) or (duty_ratio == 0.9 and pitch_LB == 7):
				b_UB, g0_UB = b_LB, g0_LB
			elif (duty_ratio == 0.53 and pitch_UB == 1.4) or (duty_ratio == 0.9 and pitch_UB == 1.3):
				b_UB, g0_UB = b_LB, g0_LB
			else:
				b_UB, g0_UB = self._load_fiber_parameter(duty_ratio, pitch_UB, center_wl, beta_degree)
			beta_n = b_LB + (b_UB - b_LB) / (pitch_UB - pitch_LB) * (now_pitch - pitch_LB)
			g0 = g0_LB + (g0_UB - g0_LB) / (pitch_UB - pitch_LB) * (now_pitch - pitch_LB)
			beta_2.append(beta_n[1])
			beta_3.append(beta_n[2])
			beta_4.append(beta_n[3])
			gamma.append(g0)

		return tuple(beta_2), tuple(beta_3), tuple(beta_4), tuple(gamma)

	def cal_gamma_Aeff(self,Aeff, center_wl):
		gamma = []
		n2 = 2.6e-20
		center_wl_um = center_wl / 1000  # um
		omiga0 = 2 * np.pi * self._c_um_s / center_wl_um
		for area0 in Aeff:
			area0 = area0 * 1e-12
			g = n2 * omiga0 / self._c_m_s / area0
			gamma.append(g)
		return gamma

	def init_pulse(self,pulse_shape='sech',frep_MHz=100, FWHM_ps=1, center_wavelength_nm=1030,
	               EPP_nj=0.1,time_window_ps = 10., GDD = 0, TOD = 0, chirp2 = 0, chirp3 = 0,
	               NPTS = 2**10):
		if pulse_shape.lower()=='sech':
			pulse_fn = pynlo.light.DerivedPulses.SechPulse
			FWHM_t0_r = 1.763
		elif pulse_shape.lower()=='gaussian':
			pulse_fn = pynlo.light.DerivedPulses.GaussianPulse
			FWHM_t0_r = 1.665
		elif pulse_shape.lower()=='sinc':
			pulse_fn = pynlo.light.DerivedPulses.SincPulse
			FWHM_t0_r =1 #3.7909885
		else:
			raise ('Invalid pulse shape! only accept "sech" or "gaussian" or "sinc"')

		self.pulse = pulse_fn(1, FWHM_ps/FWHM_t0_r, center_wavelength_nm,
                 time_window_ps = time_window_ps, frep_MHz = frep_MHz, NPTS = NPTS,
                 GDD = GDD, TOD = TOD, chirp2 = chirp2, chirp3 = chirp3,
                 power_is_avg = False)
		self.pulse.set_epp(EPP_nj*1e-9)

	def init_fiber(self,length_mm=100,center_wavelength_nm=1030,beta_2=(0,),beta_3=(0,),beta_4=(0,),gamma_W_m=(0,),alpha_db_cm=0.0,gvd_units='ps^n/m'):
		self.length = length_mm
		self.fibers=[]
		alpha =  np.log((10**(alpha_db_cm * 0.1))) * 100  # convert from dB/cm to 1/m

		assert len(beta_2) == len(beta_3) == len(beta_4) == len(gamma_W_m)

		for ii in range(len(beta_2)):
			betas = (beta_2[ii],beta_3[ii],beta_4[ii])
			fiber1 = pynlo.media.fibers.fiber.FiberInstance()
			fiber1.generate_fiber(length_mm * 1e-3, center_wl_nm=center_wavelength_nm, betas=betas,
			                      gamma_W_m=gamma_W_m[ii], gvd_units=gvd_units, gain=-alpha)
			self.fibers.append(fiber1)

	def plot_result(self,path):

		pulse = self.pulse
		pulse_out = self.pulse_out
		y = self.y_out
		AW = self.AW_out
		AT = self.AT_out

		F = pulse.F_THz  # Frequency grid of pulse (THz)
		zW = self._dB(np.transpose(AW)[:, (F > 0)])
		zT = self._dB(np.transpose(AT))
		y_mm = y * 1e3  # convert distance to mm

		fig = plt.figure(figsize=(10, 10))
		ax0 = plt.subplot2grid((3, 2), (0, 0), rowspan=1)
		ax1 = plt.subplot2grid((3, 2), (0, 1), rowspan=1)
		ax2 = plt.subplot2grid((3, 2), (1, 0), rowspan=2, sharex=ax0)
		ax3 = plt.subplot2grid((3, 2), (1, 1), rowspan=2, sharex=ax1)

		ax0.plot(pulse_out.F_THz, self._dB(pulse_out.AW), color='r',label='pulse_out')
		ax1.plot(pulse_out.T_ps, self._dB(pulse_out.AT), color='r',label='pulse_out')

		ax0.plot(pulse.F_THz, self._dB(pulse.AW), color='b',label='pulse_input')
		ax1.plot(pulse.T_ps, self._dB(pulse.AT), color='b',label='pulse_input')

		extent = (np.min(F[F > 0]), np.max(F[F > 0]), 0, self.length)
		ax2.imshow(zW, extent=extent,
		           vmin=np.max(zW) - 40.0, vmax=np.max(zW),
		           aspect='auto', origin='lower')

		extent = (np.min(pulse.T_ps), np.max(pulse.T_ps), np.min(y_mm), self.length)
		ax3.imshow(zT, extent=extent,
		           vmin=np.max(zT) - 40.0, vmax=np.max(zT),
		           aspect='auto', origin='lower')

		ax0.set_ylabel('Intensity (dB)')
		ax0.set_ylim(- 80, 0)
		ax1.set_ylim(- 40, 40)

		ax2.set_ylabel('Propagation distance (mm)')
		ax2.set_xlabel('Frequency (THz)')
		ax2.set_xlim(0, 400)

		ax3.set_xlabel('Time (ps)')

		#plt.legend()
		plt.savefig(path+'pulse_evolution.png')
		plt.show()


	def propogation(self,n_steps=100,Raman=True,self_steepening=True, local_error=0.001, save_data=False):
		self.evol = pynlo.interactions.FourWaveMixing.SSFM.SSFM(local_error=local_error, USE_SIMPLE_RAMAN=True,
		                                                   disable_Raman=np.logical_not(Raman),
		                                                   disable_self_steepening=np.logical_not(self_steepening))

		pulse_out = self.pulse
		y_out, AW_out, AT_out = None, None, None
		for fiber in self.fibers:
			y, AW, AT, pulse_out = self.evol.propagate(pulse_in=pulse_out, fiber=fiber, n_steps=n_steps)
			if y_out is None:
				y_out, AW_out, AT_out =y, AW, AT
			else:
				y_out = np.concatenate([y_out,y],axis=0)
				AW_out = np.concatenate([AW_out, AW], axis=1)
				AT_out = np.concatenate([AT_out, AT], axis=1)

		self.pulse_out = pulse_out
		self.y_out = y_out
		self.AW_out = AW_out
		self.AT_out = AT_out

		path = 'result/'
		if not os.path.exists(path):
			os.mkdir(path)
		self.plot_result(path)

		if save_data:
			import joblib
			path = path +'result.pkl'
			save_dict = {'pulse_out':pulse_out, 'y_out':y_out,'AW_out':AW_out,'AT_out':AT_out}
			joblib.dump(save_dict,path,compress=6)







