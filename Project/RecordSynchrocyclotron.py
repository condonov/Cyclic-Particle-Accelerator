import log
import numpy as np
import scipy.constants as const
import matplotlib.pyplot as plt
import copy
from EMField import EMField
from ProtonBunch import ProtonBunch

field = EMField([50*10**3,0,0], [0,0,2.82], [-0.05,0.05], 7*np.pi/4) 
protons = ProtonBunch(120*10**(6),100)

log.logger.info('Initial average kinetic energy: %s eV' % protons.KineticEnergy())
log.logger.info('Initial average momentum: %s kg m/s' % protons.momentum())
log.logger.info('Initial average position %s m' % protons.averagePosition())
log.logger.info('Initial bunch position spread: %s m' % protons.positionSpread())
log.logger.info('Initial bunch energy spread: %s eV' % protons.energySpread())

method = 2
time, deltaT, duration = 0, 10**(-11), 2.38*10**(-8)*100

inital_bunch = copy.deepcopy(protons)

timeSeries = [0.]
Data = [inital_bunch]

log.logger.info('starting simulation')
while time <= duration:
    dt = protons.adaptiveStep(deltaT,field)
    time += dt
    timeSeries.append(time)
    field.getAcceleration(protons.bunch, time, dt)
    protons.update(dt,field,time,method)
    temp_bunch = copy.deepcopy(protons)
    Data.append(temp_bunch)

log.logger.info('simulation finished')

log.logger.info('Final average kinetic energy: %s eV' % protons.KineticEnergy())
log.logger.info('Final average momentum: %s kg m/s' % protons.momentum())
log.logger.info('Final average position %s m' % protons.averagePosition())
log.logger.info('Final bunch position spread: %s m' % protons.positionSpread())
log.logger.info('Final bunch energy spread: %s eV' % protons.energySpread())

log.logger.info('writing lists to file')
np.savez('synchrocyclotron_data', time=timeSeries, protons_data=Data)
log.logger.info('file writing complete')