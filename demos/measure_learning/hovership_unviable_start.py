import slippy.hovership as true_model
import numpy as np
import pickle

import plotting.corl_plotters as cplot

import measure.active_sampling as sampling

def run_demo(dynamics_model_path = './data/dynamics/', gp_model_path = './data/gp_model/', results_path='./results/'):

    ################################################################################
    # Load model data
    ################################################################################

    dynamics_file = dynamics_model_path + 'hover_map.pickle'
    gp_model_file = gp_model_path + 'hover_prior.npy'

    infile = open(dynamics_file, 'rb')
    data = pickle.load(infile)
    infile.close()

    # TODO Make model fit API (S)
    true_model.mapSA2xp = true_model.sa2xp
    true_model.map2s = true_model.xp2s

    # A prior state action pair that is considered safe (from system knowledge)
    # Here it is chosen to be outside the viable set to demonstrate that the learner can deal with this case
    X_seed = np.atleast_2d(np.array([.4, 1.5]))
    y_seed = np.array([[.75]])

    seed_data = {'X': X_seed, 'y': y_seed}

    sampler = sampling.MeasureLearner(model=true_model, model_data=data)
    sampler.init_estimation(seed_data=seed_data,
                            prior_model_path=gp_model_file,
                            learn_hyperparameters=False)

    sampler.exploration_confidence_s = 0.94
    sampler.exploration_confidence_e = 0.999
    sampler.measure_confidence_s = 0.80
    sampler.measure_confidence_e = 0.999
    sampler.safety_threshold_s = 0.0
    sampler.safety_threshold_e = 0.0

    n_samples = 250

    # To avoid accidental overwriting of data
    random_string = str(np.random.randint(1, 10000))

    plot_callback = cplot.create_plot_callback(n_samples,
                                               experiment_name='hovership_unviable_start',
                                               random_string=random_string,
                                               save_path=results_path)

    s0 = 1.5
    sampler.run(n_samples=n_samples, s0=s0, callback=plot_callback)