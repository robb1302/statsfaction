import tensorflow as tf
import tensorflow as tf
from sklearn.metrics import f1_score



def macro_f1(y_true, y_pred):
    y_pred = tf.argmax(y_pred, axis=-1)
    y_true = tf.argmax(y_true, axis=-1)
    f1 = tf.py_function(lambda y_true, y_pred: f1_score(y_true, y_pred, average='macro'), 
                        [y_true, y_pred], 
                        Tout=tf.float32, 
                        name='custom_f1_score')
    return f1


class BinaryF1Score(tf.keras.metrics.Metric):
    def __init__(self, name='binary_f1_score', **kwargs):
        super().__init__(name=name, **kwargs)
        self.true_positives = self.add_weight(name='tp', initializer='zeros')
        self.false_positives = self.add_weight(name='fp', initializer='zeros')
        self.false_negatives = self.add_weight(name='fn', initializer='zeros')

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = tf.cast(y_true, tf.bool)
        y_pred = tf.cast(y_pred, tf.bool)

        true_positives = tf.reduce_sum(tf.cast(tf.logical_and(y_true, y_pred), self.dtype))
        false_positives = tf.reduce_sum(tf.cast(tf.logical_and(tf.logical_not(y_true), y_pred), self.dtype))
        false_negatives = tf.reduce_sum(tf.cast(tf.logical_and(y_true, tf.logical_not(y_pred)), self.dtype))

        if sample_weight is not None:
            sample_weight = tf.cast(sample_weight, self.dtype)
            true_positives = tf.multiply(true_positives, sample_weight)
            false_positives = tf.multiply(false_positives, sample_weight)
            false_negatives = tf.multiply(false_negatives, sample_weight)

        self.true_positives.assign_add(true_positives)
        self.false_positives.assign_add(false_positives)
        self.false_negatives.assign_add(false_negatives)

    def result(self):
        precision = self.true_positives / (self.true_positives + self.false_positives + tf.keras.backend.epsilon())
        recall = self.true_positives / (self.true_positives + self.false_negatives + tf.keras.backend.epsilon())
        f1_score = 2 * (precision * recall) / (precision + recall + tf.keras.backend.epsilon())
        return f1_score

    def reset_states(self):
        self.true_positives.assign(0)
        self.false_positives.assign(0)
        self.false_negatives.assign(0)


class MacroF1Score(tf.keras.metrics.Metric):
    def __init__(self, name='macro_f1_score', num_classes=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.num_classes = num_classes
        self.true_positives = [self.add_weight(name='tp_' + str(i), initializer='zeros') for i in range(num_classes)]
        self.false_positives = [self.add_weight(name='fp_' + str(i), initializer='zeros') for i in range(num_classes)]
        self.false_negatives = [self.add_weight(name='fn_' + str(i), initializer='zeros') for i in range(num_classes)]

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = tf.argmax(y_true, axis=1)
        y_pred = tf.argmax(y_pred, axis=1)

        for i in range(self.num_classes):
            true_positives = tf.reduce_sum(tf.cast(tf.logical_and(tf.equal(y_true, i), tf.equal(y_pred, i)), self.dtype))
            false_positives = tf.reduce_sum(tf.cast(tf.logical_and(tf.not_equal(y_true, i), tf.equal(y_pred, i)), self.dtype))
            false_negatives = tf.reduce_sum(tf.cast(tf.logical_and(tf.equal(y_true, i), tf.not_equal(y_pred, i)), self.dtype))

            if sample_weight is not None:
                sample_weight = tf.cast(sample_weight, self.dtype)
                true_positives *= sample_weight
                false_positives *= sample_weight
                false_negatives *= sample_weight

            self.true_positives[i].assign_add(tf.reduce_sum(true_positives))
            self.false_positives[i].assign_add(tf.reduce_sum(false_positives))
            self.false_negatives[i].assign_add(tf.reduce_sum(false_negatives))

    def result(self):
        true_positives = tf.reduce_sum(self.true_positives)
        false_positives = tf.reduce_sum(self.false_positives)
        false_negatives = tf.reduce_sum(self.false_negatives)

        precision = true_positives / (true_positives + false_positives + tf.keras.backend.epsilon())
        recall = true_positives / (true_positives + false_negatives + tf.keras.backend.epsilon())
        f1_score = 2 * (precision * recall) / (precision + recall + tf.keras.backend.epsilon())

        return f1_score
