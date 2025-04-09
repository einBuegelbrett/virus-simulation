import covasim as cv

def protect_elderly(sim):
    if sim.t == sim.day('2020-07-30'):
        elderly = sim.people.age > 70
        sim.people.rel_sus[elderly] *= 0.1

def mask_wearing(sim):
    if sim.t == sim.day('2020-09-01'):
        sim['beta'] *= 0.95

    # if sim.t == sim.day('2020-07-01'):
    #     sim['beta'] /= 0.5

def lockdown(sim):
    if sim.t == sim.day('2020-03-22'):
        sim['beta'] *= 0.6
    
    if sim.t == sim.day('2020-05-04'):
        sim['beta'] /= 0.6

# Testing and contact tracing interventions ==> Quarantine
tp = cv.test_prob(symp_prob=0.1, asymp_prob=0.01)
ct = cv.contact_tracing(trace_probs=0.5, trace_time=2)

pfizer = cv.vaccinate_prob(vaccine='pfizer', days=30*9, prob=0.8)

def hospital_beds(sim):
    if sim.t == sim.day('2020-03-01'):
        sim['n_beds_hosp'] = 1000
        sim['n_beds_icu'] = 500

if __name__ == "__main__":
    pars = {
            'pop_type': 'hybrid',
            'location': 'germany',
            'pop_size': 60e3, 
            'start_day': '2020-09-01', 
            'n_days': 210,
            # 'beta': 0.01,
            }

    alpha = cv.variant(variant={'rel_beta': 1}, label='Alpha', days=0, n_imports=10)
    delta = cv.variant(variant={'rel_beta': 2.1}, label='Delta', days=30*5, n_imports=10)

    # sim1 = cv.Sim(pars=pars, variants=[alpha], label='Default', analyzers=cv.age_histogram())
    # sim2 = cv.Sim(pars=pars, variants=[alpha], label='Protect elderly', interventions=[protect_elderly, hospital_beds], analyzers=cv.age_histogram())
    # sim3 = cv.Sim(pars=pars, variants=[alpha], label='Mask wearing', interventions=[mask_wearing, hospital_beds], analyzers=cv.age_histogram())
    # sim4 = cv.Sim(pars=pars, variants=[alpha], label='Lockdown', interventions=[lockdown, hospital_beds], analyzers=cv.age_histogram())
    # sim5 = cv.Sim(pars=pars, variants=[alpha], label='Quarantine', interventions=[tp,ct, hospital_beds], analyzers=cv.age_histogram())
    # multiSim = cv.MultiSim([sim1, sim2, sim3, sim4, sim5])
    # multiSim.run().plot(to_plot=['cum_deaths', 'cum_infections', 'new_infections', 'new_deaths'])

    combinedSim = cv.Sim(pars=pars, 
                         variants=[alpha, delta], 
                         label='Combined', 
                         interventions=[protect_elderly, tp, ct, hospital_beds, mask_wearing, lockdown, pfizer], 
                         analyzers=cv.age_histogram(),
                         use_waning=True,
                        #  nab_decay=dict(form='nab_growth_decay', growth_time=21, decay_rate1=0.07, decay_time1=47, decay_rate2=0.02, decay_time2=106),
                         )
    combinedSim.run().plot(to_plot=['cum_deaths', 'cum_infections', 'new_infections', 'new_deaths'])

    maskLockdownSim = cv.Sim(pars=pars,
                variants=[alpha, delta],
                label='Mask wearing',
                interventions=[mask_wearing, hospital_beds, lockdown],
                analyzers=cv.age_histogram(),
                use_waning=True,
                # nab_decay=dict(form='nab_growth_decay', growth_time=21, decay_rate1=0.07, decay_time=47, decay_rate2=0.02, decay_time2=106),
                )
    maskLockdownSim.run().plot(to_plot=['cum_deaths', 'cum_infections', 'new_infections', 'new_deaths'])
    
    freeSim = cv.Sim(pars=pars,
                     variants=[alpha, delta],
                     label='Free',
                     interventions=[hospital_beds],
                     analyzers=cv.age_histogram(),
                     use_waning=True,
                     # nab_decay=dict(form='nab_growth_decay', growth_time=21, decay_rate1=0.07, decay_time1=47, decay_rate2=0.02, decay_time2=106),
                     )
    freeSim.run().plot(to_plot=['cum_deaths', 'cum_infections', 'new_infections', 'new_deaths'])


    # analyzeSim = sim2
    # analyzeRun = analyzeSim.run()

    # cv.plotly_animate(analyzeSim)

    # tt1 = analyzeRun.make_transtree()
    # tt1.plot_histograms()

    # hist1 = analyzeSim.get_analyzer()
    # hist1.plot()