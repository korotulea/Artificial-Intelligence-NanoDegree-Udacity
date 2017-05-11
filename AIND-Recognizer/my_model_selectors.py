import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """
    def bic_criteria(self, log_likelihood, n_parameters, n_points):
        """
        This function return Bayesian information ctireria
        Input: log_likelihood, number of parameters, number of data points
        """
        return -2 * log_likelihood + n_parameters * math.log(n_points)
    
    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        # TODO implement model selection based on BIC scores
        n_points = len(self.X) # https://discussions.udacity.com/t/number-of-data-points-bic-calculation/235294/3
        best_model = None
        bic_best = float("inf")
        # iterate components from min to max and compute BIC score
        for n_components_tmp in range(self.min_n_components, self.max_n_components + 1):
            try:
                model_tmp = self.base_model(n_components_tmp)
                logL_tmp = model_tmp.score(self.X, self.lengths)
                n_parameters_tmp =  (n_components_tmp ** 2) + (2 * n_components_tmp * n_points) - 1 # https://discussions.udacity.com/t/number-of-parameters-bic-calculation/233235/6
                bic_tmp = self.bic_criteria(logL_tmp, n_parameters_tmp, n_points)
                # compare previous model BIC score with current and update best model in case of smaller BIC score
                if bic_tmp <= bic_best:
                    best_model = model_tmp  
                    bic_best = bic_tmp
            except:
                pass
        print('Best BIC score:{} for {}'.format(bic_best, self.this_word))
        return best_model
            
class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        # TODO implement model selection based on DIC scores
        best_model = None
        dic_best = - float("inf")
        # iterate components from min to max
        for n_components_tmp in range(self.min_n_components, self.max_n_components + 1):
            try:
                model_tmp = self.base_model(n_components_tmp)
                logL = model_tmp.score(self.X, self.lengths)
                logL_others = []
                # compute logL for all other words and add values to the logL_others list
                for word_tmp in self.hwords:
                    if word_tmp != self.this_word:
                        X_tmp, lengths_tmp = self.hwords[word_tmp]
                        logL_others.append(model_tmp.score(X_tmp, lengths_tmp))
                dic_tmp = logL - np.mean(logL_others)
                # if difference of logL for the word of interest and mean of logL of this models for other words is bigger than difference of the best model, the new model is better
                if dic_tmp >= dic_best:
                    best_model = model_tmp
                    dic_best = dic_tmp
            except:
                pass        
        print('Best DIC score:{} for {}'.format(dic_best, self.this_word))
        return best_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        # TODO implement model selection using CV
        best_model = None
        score_best_cv = - float("inf")
        # iterate components from min to max
        for n_components_tmp in range(self.min_n_components, self.max_n_components + 1):
            if len(self.sequences) > 2: # check if it is enough to split
                split_method = KFold(n_splits=3) 
                #print('split 3', self.this_word)
            else:
                #print('split 2', self.this_word)
                split_method = KFold(n_splits=2)
            model_tmp = GaussianHMM(n_components=n_components_tmp, covariance_type="diag", n_iter=1000, random_state=self.random_state, verbose=False)
            logL_test_list = []
            try:
                for cv_train_idx_tmp, cv_test_idx_tmp in split_method.split(self.sequences):
                    # prepare train dataset
                    X_train_tmp, lengths_train_tmp = combine_sequences(cv_train_idx_tmp, self.sequences)
                    # train model
                    model_cv_tmp = model_tmp.fit(X_train_tmp, lengths_train_tmp)
                    # prepare test datset
                    X_test_tmp, lengths_test_tmp = combine_sequences(cv_test_idx_tmp, self.sequences)
                    # compute log likelihood and apped to the list of already computed logL
                    log_L_tmp = model_cv_tmp.score(X_test_tmp, lengths_test_tmp)
                    logL_test_list.append(log_L_tmp)   
                    #print('CV-score:', log_L_tmp)
                score_best_cv_tmp = np.mean(logL_test_list)
                #print(self.this_word, n_components_tmp)
                #print('meanCV-score:',score_best_cv_tmp, 'Best-score:', score_best_cv)
                # choose model with maximum logL mean of the CV
                if score_best_cv_tmp >= score_best_cv:
                    best_model = model_tmp 
                    score_best_cv = score_best_cv_tmp
            except:
                pass
        print('Best mean CV score:{} for {}'.format(score_best_cv, self.this_word))
        return best_model
