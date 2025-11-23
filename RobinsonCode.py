import numpy as np
import time
import PlotAntPath as pap

def RobinsonCode(n, quals, probs, threshold_mean, threshold_stddev, qual_stddev, time_means, time_stddevs, ToPlot, quora):
    #   n = number of replicates (>=1)
    #   quals = row vector of m site qualities
    #		(quals(1) = home site
    #     	quality: -Inf for no effect of home site quality on searching)
    #   discovery_probabilities = m * m matrix of discovery probabilities from
    #     column site to row site (N.B. columns should sum to 1)
    #   threshold_mean: mean population threshold for site acceptability
    #   threshold_stddev: standard deviation in population thresholds
    #   qual_stddev: standard deviation in quality assessments: **AOP**
    #   time_means: m * m matrix of mean travel times from column site to row
    #     site (N.B. should probably be symmetric)
    #   time_stddevs: m * m matrix of travel time standard deviations, from
    #     column site to row site (N.B. should probably be symmetric)
    #   quora: 1 * m matrix of quorum times for each nest site
    #
    #   times = row vector of times to first recruitment (i.e. nest acceptance)
    #   discovers = matrix (m x i) of times of first visit to each site
    #   visits = matrix (m x i) of numbers of visits to each site
    #   accepts = row vector of ids of accepted sites (indexed from 1 (for home nest) to m)
    #   the equivalents prefixed 'preq' are the pre-quorum equivalents of these

    # MATLAB allows variables to be created (and to grow) implicitly when elements are assigned
    # - Python doesn't play that foolish game, so we have to assign some variables here which we didn't in MATLAB
    nestNum = probs.shape[0]
    accepts = np.zeros([n], dtype=int)
    current_time = np.zeros([n])
    discovers = np.zeros([nestNum, n])
    visits = np.zeros([nestNum, n])

    Ants = []
    for i in range(n):
        ant = {'path': [],
               't': [],
               'thresh': 0,
               'selected': 0}
        Ants.append(ant)

    # set the random number generator to a new random state **AOP**
    rnd_seed = int(time.time())
    np.random.seed(rnd_seed)

    # corresponds to line 27 in m-code
    # Set the maximum number of steps for each ant
    Max_num_steps = 1000

    # corresponds to line 34 in m-code
    for i in range(n): # note that Python indexing is from 0, whereas MATLAB is from 1

        # Monte Carlo simulation of one ant
        # this sets up the output variables **AOP**

        # This holds the time it has taken before an ant has made the first
        # recruitment **AOP**
        current_time[i] = 0

        # this is a variable which holds where ant i currently is **AOP**
        accepts[i] = 0 # ant starts in home site

        # this is a matrix which holds the time at which the ant discovers
        # sites 1 to N where N= number of sites;
        # As ant is currently in the home site it never 'discovers' it
        # so set this (arbitrarily) to -1 **AOP**
        discovers[0,i] = -1 # ant is already in home site

        # this is a matrix which holds the number of times an ant visits
        # sites 1 to number of sites. As it is already in the home site the
        # 1st element is set to 1 **AOP**
        visits[0,i] = 1 # ant is already in home site

        # These are to do with the quorum sensing bit:
        # currently we're not using **AOP**
        # unless you're adapting the quorum bit then ignore
        # preqtimes[i] = 0;
        # preqaccepts[i] = 1;
        # preqdiscovers[0,i] = -1;
        # preqvisits[0,i] = 1;

        # initialise the variables for the other home sites. it hasn't been to
        # any of the others so the time to 1st discovery is 0 and the number
        # of visits = 0  **AOP**
        for j in range(1, nestNum): # could be a problem here?
            discovers[j,i] = 0 # ant has not discovered or visited other sites
            visits[j,i] = 0
            # preqdiscovers[j,i] = 0;
            # preqvisits[j,i] = 0;

        # sample and set the ant's acceptance threshold **AOP**
        thresh = threshold_stddev * np.random.randn() + threshold_mean

        # set up some output variables *** AOP
        num_step = 0
        Ants[i]['path'].append(accepts[i])
        Ants[i]['t'].append(current_time[i])
        Ants[i]['thresh'] = thresh
        Ants[i]['selected'] = 0


        # corresponds to line 87 in m-code
        # this is now the main loop of the program. Essentially it says:
        # 1. for the current site, check to see if the ant accepts it based on
        #    it's threshold and a randomly selected quality based on the quality
        #    of the site **AOP**
        # 2. Do this until a site is accepted
        while Ants[i]['selected'] == 0:

            # check the quality of the current nest
            perceivedQuality = qual_stddev[accepts[i]] * np.random.randn() + quals[accepts[i]]

            # if the perceived nest quality is above the threshold, select it
            if perceivedQuality >= Ants[i]['thresh']:
                Ants[i]['selected'] = 1
                break

            # Plot the current state. To always skip **AOP**
            # set ToPlot=0 above or comment this bit out
            if ToPlot != 0 and ToPlot != 1:
                pap.PlotAntPath(Ants[i], perceivedQuality)
                print(' ')
                print('press return to continue')
                print('enter 1 to skip to next ant: ')
                try:
                    ToPlot = int(input('or enter 0 to go to summary: '))
                except:
                    ToPlot = None

            # if you have exceeded the max number of steps without stopping
            # break out of the algorithm
            if num_step > Max_num_steps:
                Ants[i]['selected'] = 0
                break

            # probablistically pick one of the new sites to go to
            # unifrnd(0,1) generates a uniformly distributed number
            # between 0 and 1
            ran = np.random.uniform()
            # this then does the site picking. Looks complicated but is standard
            # and it works
            newsite = 0 # NOTE: THIS IS 0 INSTEAD OF 1 DUE TO PYTHON INDEXING!
            while ran > probs[newsite, accepts[i]]:
               ran = ran - probs[newsite, accepts[i]]
               newsite = newsite + 1

            # update the time taken with normally-distributed time-step size
            # (>=1) **AOP**
            delta = max(1, time_stddevs[newsite, accepts[i]] * np.random.randn() + time_means[newsite, accepts[i]])
            current_time[i] = current_time[i] + delta

            # update ant's current site, accepts, **AOP**
            # discovers, and the number of times it has been visited, visits **AOP**
            accepts[i] = newsite

            # if it hasn't discovered this site before, update the time that it
            # 1st discovered it, in discovers **AOP**
            if discovers[newsite, i] == 0:
               discovers[newsite, i] = current_time[i]

            # update the number of times it has visited this site **AOP**
            visits[newsite, i] = visits[newsite, i] + 1

            # Update the output variables **AOP**
            num_step = num_step + 1
            Ants[i]['path'].append(accepts[i])
            Ants[i]['t'].append(current_time[i])

          # this is to do with quorum sensing
          # this doesn't necessarily need using but could be adapted **AOP**
          # so ignore unless you want to do this element
    #        if times(i) > quora (1, newsite)    %if past pre-quorum period, then no new nests can be added
    #             preqtimes(i) = NaN;
    #             preqaccepts(i) = preqaccepts(i);
    #                    if preqdiscovers(newsite,i)== 0
    #                         preqdiscovers(newsite,i)= NaN;
    #                    end
    #            preqvisits(newsite,i)=preqvisits(newsite,i);
    #        else
    #            preqtimes(i)=times(i);
    #            preqaccepts(i) = newsite;
    #                    if preqdiscovers(newsite,i)== 0
    #                         preqdiscovers(newsite,i)= times(i);
    #                    end
    #            preqvisits(newsite,i)=preqvisits(newsite,i)+1;
    #        end

        # corresponds to line 176 in m-code
        # record number of steps taken
        Ants[i]['numSteps'] = num_step

        # plot the fnal path
        if ToPlot != 0:
            ToPlot = []
            pap.PlotAntPath(Ants[i], perceivedQuality)
            pl = 1
            if Ants[i]['selected'] == 1:
                strr = 'Ant ' + str(i) + ' selected site ' + str(accepts[i])
            else:
                strr = 'Ant ' + str(i) + ' did not select a site'
            while pl != 0:
                print(' ')
                print(strr)
                try:
                    pl = int(input('enter 0 to continue: '))
                except:
                    pass

    return current_time, discovers, visits, accepts, Ants, rnd_seed, [], [], [], [] # , preqtimes, preqdiscovers, preqvisits, preqaccepts
