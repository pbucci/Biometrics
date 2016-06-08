class Columns:
	def __init__(self):
		self.columns = ['Time','B: BVP','C: EMG','D: EMG','E: Skin Cond','F: Temp','G: Abd Resp','H: Thor Resp (optional)','B: BVP amplitude','B: BVP IBI','B: BVP HR from IBI','B: BVP HR (Smoothed)','B: BVP IBI peak freq.','B: BVP VLF % power','B: BVP LF % power','B: BVP HF % power','B: BVP VLF Total power','B: BVP LF Total power','B: BVP HF Total power','C: EMG + Smoothing','D: EMG + Smoothing','C&D: C:EMG - D:EMG','C&D: C:EMG + D:EMG','C&D: EMG C-D/C+D (balance fb)','E: SC as % of value','F: Temp as % of value','G: Resp Amplitude (Abd)','G: Resp period','G: Resp rate','B&G: HR max - HR min','H: Resp amplitude (thor)','G&H: Abd - Thor amplitude diff','B: BVP HR epoch mean','B: BVP IBI epoch std dev','B: BVP VLF % power ep mean','B: BVP LF % power ep mean','B: BVP HF % power ep mean','B: BVP VLF Total power ep mean','B: BVP LF Total power ep mean','B: BVP HF Total power ep mean','B: BVP LF/HF (ep means)','C: EMG epoch mean','D: EMG epoch mean','E: SC epoch mean','F: Temp epoch mean','G: Resp rate epoch mean','B: BVP amplitude mean (Rel)','B: BVP HR mean (beats/min)','B: BVP HR std. dev.','B: BVP peak freq. mean (Hz)','B: BVP IBI std. dev. (SDRR)','B: BVP VLF % power mean','B: BVP LF % power mean','B: BVP HF % power mean','B: BVP VLF total power mean','B: BVP LF Total power mean','B: BVP HF total power mean','B: BVP LF/HF (means)','C: EMG mean (uV)','D: EMG mean (uV)','E: Skin conductance mean (uS)','E: SC as % of value mean (%)','F: Temperature mean (Deg)','F: Temp as % of value mean (%)','G: Resp rate mean (br/min)','B&G: (HR max-min) mean (b/min)','G: Abd amplitude mean (rel)','H: Thor amplitude mean (rel)','G&H: Abd-tho ampl diff (means)','B: BVP IBI Peak amplitude','B: BVP IBI Pk ampl maximum','B: BVP IBI pk freq trigger','B: BVP IBI pk ampl trigger','H: Resp rate trigger','B: BVP IBI NN Intervals','B: BVP IBI pNN Intervals','B: BVP IBI pNN Intervals (%)']
	
	def getColumns(self):
		return self.columns

	def searchColumns(self,sterm):
		return [x for x in self.columns if x.find(sterm) > -1]

	def selectColumn(self,sterm):
		ret = self.searchColumns(sterm)
		if len(ret) == 1:
			ind = ret[0]
			i = 0
			for j in self.columns:
				if j == ind:
					return i
				i = i + 1
			return (-1)
		else:
			return (-1)