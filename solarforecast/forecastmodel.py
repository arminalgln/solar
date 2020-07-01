# =============================================================================
# class for model
# =============================================================================
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
# from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model
import numpy as np
class Solar():
    """
    This is a class for forecasting solar irrediation    
    """
    def __init__(self):
        self.model=model=self.__make_model()

    # private funciton to make model
    def __make_model(self):
        model=keras.Sequential(
            [
                layers.Dense(32,activation='relu',name='dense_layer_1'),
                layers.Dense(128,activation='relu',name='dense_layer_2'),
                layers.Dense(128,activation='relu',name='dense_layer_3'),
                layers.Dense(24,activation='relu',name='output'),
                ])
        return model
    
    def opt_ls_mtr(self,**kwarg):
        """

        Parameters
        ----------
        **kwarg : string
            optimizer, loss and metric.

        Returns
        -------
        None.

        """
        opt,ls,mtr=kwarg['optimizer'],kwarg['loss'],kwarg['metric']
        self.model.compile(
            optimizer=keras.optimizers.get(opt),
            loss=keras.losses.get(ls),
            metrics=[keras.metrics.get(mtr)],
            )
    
    def train(self,inp,out,**kwarg):
        """

        Parameters
        ----------
        inp : matrix
            features that can be used for train, dev and test dataset.
        out : vector
            solar irrediation.
        **kwarg : integer
            batch and epoch.

        Returns
        -------
        Training calculation based on the **kwarg numbers

        """
        batch,epoch=kwarg['batch'],kwarg['epoch']
        self.model.fit(
            inp,
            out,
            batch_size=batch,
            epochs=epoch
            )
    
    
    def solar_eval(self,inp,out):
        """

        Parameters
        ----------
        inp : matrix
            features for evaluation such as training, dev or test set.
        out : matrix
            True values to evaluate the predicted values.

        Returns
        -------
        TYPE
            evaluation.

        """
        return self.model.evaluate(inp,out)
    
    
    def solar_predict(self,x_pred):
        """
        
        Parameters
        ----------
        x_pred : matrix
            features for prediction.

        Returns
        -------
        vector
            predicted solar irrediation.

        """
        return self.model.predict(x_pred)
    
