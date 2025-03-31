import covasim as cv

def protect_elderly(sim):
    if sim.t == sim.day('2020-03-15'):
        elderly = sim.people.age > 70
        sim.people.rel_sus[elderly] = 0.1

def mask_wearing(sim):
    if sim.t == sim.day('2020-03-15'):
        sim['beta'] *= 0.5

def lockdown(sim):
    if sim.t == sim.day('2020-03-15'):
        sim['beta'] *= 0.5

# Testing and contact tracing interventions ==> Quarantine
tp = cv.test_prob(symp_prob=0.1, asymp_prob=0.01)
ct = cv.contact_tracing(trace_probs=0.5, trace_time=2)

if __name__ == "__main__":
    pars = {
            'pop_size': 50e3, 
            'start_day': '2020-02-01', 
            'n_days': 120
            }
    sim1 = cv.Sim(pars=pars, label='Default', analyzers=cv.age_histogram())
    sim2 = cv.Sim(pars=pars, label='Protect elderly', interventions=protect_elderly, analyzers=cv.age_histogram())
    sim3 = cv.Sim(pars=pars, label='Mask wearing', interventions=mask_wearing, analyzers=cv.age_histogram())
    sim4 = cv.Sim(pars=pars, label='Lockdown', interventions=lockdown, analyzers=cv.age_histogram())
    sim5 = cv.Sim(pars=pars, label='Quarantine', interventions=[tp,ct], analyzers=cv.age_histogram())
    multiSim = cv.MultiSim([sim1, sim2, sim3, sim4, sim5])
    multiSim.run().plot(to_plot=['cum_deaths', 'cum_infections'])

    analyzeSim = sim2
    analyzeRun = analyzeSim.run()

    cv.plotly_animate(analyzeSim)

    tt1 = analyzeRun.make_transtree()
    tt1.plot_histograms()

    hist1 = analyzeSim.get_analyzer()
    hist1.plot()