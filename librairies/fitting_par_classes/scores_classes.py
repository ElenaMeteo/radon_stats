""" Dans ce fichier calcule les scores relatifs aux
fitting des distributions simples et doubles."""

class Scores:
    """Classe pour calculer les scores relatifs aux 
    fitting des distributions simples et doubles. """

    def __init__(self):
        self.resultats_simple_auto = None
        self.resultats_simple_manuel = None
        self.resultats_double = None

    def aic(self):
    

    def best_fit(self):
        """Retourne le meilleur fitting selon les scores AIC et BIC. """
        best_fit = {}
        if self.resultats_simple_auto:
            best_fit['simple_auto'] = min(self.resultats_simple_auto, key=lambda x: (x['aic'], x['bic']))
        if self.resultats_simple_manuel:
            best_fit['simple_manuel'] = min(self.resultats_simple_manuel, key=lambda x: (x['aic'], x['bic']))
        if self.resultats_double:
            best_fit['double'] = min(self.resultats_double, key=lambda x: (x['aic'], x['bic']))
        return best_fit
    
    def return_scores(self):
        """Retourne les scores AIC pour les différents types de fitting. """
        return 
        {"simple_auto": [res['aic'] for res in self.resultats_simple_auto] if self.resultats_simple_auto else None,
            "simple_manuel": [res['aic'] for res in self.resultats_simple_manuel] if self.resultats_simple_manuel else None,
            "double": [res['aic'] for res in self.resultats_double] if self.resultats_double else None}