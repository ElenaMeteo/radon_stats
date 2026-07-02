# Source - https://stackoverflow.com/a/79326808
# Posted by MuhammedYunus, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-19, License - CC BY-SA 4.0

import numpy as np

from scipy.stats import gamma, rv_continuous
from scipy.special import softmax
from scipy.optimize import minimize
import json
import sys
from typing import Tuple

# classe de fonction pour une unique fonction gamma
class gamma_solo(rv_continuous):
    def _pdf(self, x, a1, scale1):
        return gamma.pdf(x, a1, scale=scale1)
    
    def fit(self, data):
        def log_likelihood(params):
            eps = 1e-8
            a1, scale1 = params
            mixture = gamma.pdf(data, a1, scale=scale1)
            return -np.log(mixture+eps).mean()

        initial_params = [2.0, 2.0]
        bounds = [(0, None), (0, None)]
        result = minimize(log_likelihood, initial_params, bounds=bounds, method='L-BFGS-B')
        if result.success:
            self.fitted_params = result.x
        else:
            raise RuntimeError("Optimization failed")



# classe de fonctions pour N fonctions gamma
class GammaMixture:
    def __init__(self, n_components: int):       # initialisation des paramètres
        self.n_components = n_components
        self.weights = np.ones(n_components) / n_components
        self.alphas = np.ones(n_components)
        self.scales = np.ones(n_components)

    def _pdf(self, x: np.ndarray) -> np.ndarray:   # définition de la pdf qui est une somme de N fonctions gamma
        mixture = np.row_stack([
            self.weights[i] * gamma.pdf(x, self.alphas[i], scale=self.scales[i])
            for i in range(self.n_components)
        ]).sum(axis=0)

        return mixture

    def _negative_log_likelihood(self, params: np.ndarray, data: np.ndarray) -> float:    # construction du logarithme de la vraisemblance
        logits, self.alphas, self.scales = np.split(params, [self.n_components, 2*self.n_components])
        self.weights = softmax(logits)

        eps = 1e-8
        neg_log_likelihood = -np.log(self._pdf(data) + eps).mean()
        return neg_log_likelihood

    def fit(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:   # fonction qui fait le "fit" en appelant la fonction minimize de scipy
        initial_params = np.concatenate([
            np.log(self.weights),
            np.ones(2*self.n_components) + np.random.uniform(0, 0.01, 2*self.n_components) #break symmetry
        ])

        bounds = [(None, None)]*self.n_components + [(0, None)] * (2*self.n_components)
        result = minimize(
            self._negative_log_likelihood,
            initial_params, args=(data,), bounds=bounds
        )
        print('Success?', result['success'])

        logits, self.alphas, self.scales = np.split(result['x'], [self.n_components, 2*self.n_components])
        self.weights = softmax(logits)

        return self.weights, self.alphas, self.scales

    def sample(self, n_samples: int) -> np.ndarray:    # fonction qui permet de retourner un échantillon d'une pdf
        components = np.random.choice(self.n_components, size=n_samples, p=self.weights)
        samples = np.array([gamma.rvs(self.alphas[i], scale=self.scales[i]) for i in components])
        return samples
#
# Source - https://stackoverflow.com/a/79326808
# Posted by MuhammedYunus, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-19, License - CC BY-SA 4.0


# 1) On ouvre le fichier json de quantiles et on construit un vecteur numpy
f=open('dict_yAyB_quantiles.json')
data_dict=json.load(f)
mylist=[]
for i in range(len(data_dict["quantile_7"]["yB"])):
 for item in data_dict["quantile_7"]["yB"][i] :
  mylist.append(item)
data=np.array(mylist)

# 2) On 'fit avec une seule fonction gamma
custom_gamma = gamma_solo(name='gamma_solo')
custom_gamma.fit(data)
a1, scale1 = custom_gamma.fitted_params
print('shape : ',a1,'scale : ',scale1)
mean1, var1 = gamma.stats(a1,loc=0,scale=scale1,moments='mv')
print('moyenne : ',mean1,'variance : ',var1)

# Example usage:
np.random.seed(1)
n_per_component = 2_000
n_components = 2    # nombre de fonctions gamma 


# On définit le mélange de fonctions gamma et on fait le 'fit'
gamma_mixture = GammaMixture(n_components)
weights, alphas, scales = gamma_mixture.fit(data)

print("Fitted Parameters:")
print("Weights:", weights)
print("Alphas:", alphas)
print("Scales:", scales)

mean1, var1 = gamma.stats(alphas[0],loc=0,scale=scales[0],moments='mv')
mean2, var2 = gamma.stats(alphas[1],loc=0,scale=scales[1],moments='mv')

print('moyenne 1 : ',mean1,'variance 1 : ',var1,'moyenne 2 : ',mean2,'variance 2 : ',var2)

# Generate samples from the fitted model
samples_orig = gamma_mixture.sample(n_samples=10_000)
samples=gamma.rvs(a1,scale=scale1,size=10000)


# La partie en dessous gère l'affichage des graphiques

import matplotlib.pyplot as plt

# Plot histograms
f, ax = plt.subplots(figsize=(5, 3), layout='tight')

# Histogram of original data = les données des quantiles
ax.hist(
    data, bins=70, density=True,
    color='orange', alpha=0.8, label='original samples'
)

# Histogram of new samples = pdf avec une seule fonction gamma
ax.hist(
    samples, bins=70, density=True, histtype='step',
    color='black', linewidth=1.5, label='drawn from fitted model'
)


# Histogramme avec le pdf bi-modale
ax.hist(
    samples_orig, bins=70, density=True, histtype='step',
    color='red', linewidth=1.5, label='drawn from fitted bimodal'
)

#Formatting the figure
ax.set(xlabel='value', ylabel='Density', title='Histograms of original and generated data')
ax.legend(fontsize=9, framealpha=0)

ax.spines[['top', 'right', 'bottom']].set_visible(False)
ax.spines.left.set_bounds(0, 0.025)

plt.show()



