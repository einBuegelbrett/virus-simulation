import covasim as cv

def protect_elderly(sim):
    if sim.t == sim.day('2020-03-15'):
        elderly = sim.people.age > 70
        sim.people.rel_sus[elderly] = 0.1

def lockdown(sim):
    if sim.t == sim.day('2020-03-15'):
        sim['beta'] *= 0.5

if __name__ == "__main__":
    pars = {
            'pop_size': 10e3, 
            'start_day': '2020-02-01', 
            'n_days': 120
            }
    sim1 = cv.Sim(pars=pars, label='Default', analyzers=cv.age_histogram())
    sim2 = cv.Sim(pars=pars, label='Protect elderly', interventions=protect_elderly, analyzers=cv.age_histogram())
    sim4 = cv.Sim(pars=pars, label='Lockdown', interventions=lockdown, analyzers=cv.age_histogram())
    multiSim = cv.MultiSim([sim1, sim2, sim4])
    multiSim.run().plot(to_plot=['cum_deaths', 'cum_infections'])

    analyzeSim = sim2

    analyzeRun = analyzeSim.run()
    tt1 = analyzeRun.make_transtree()
    tt1.plot_histograms()

    hist1 = analyzeSim.get_analyzer()
    hist1.plot()