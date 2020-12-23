from allennlp.predictors.predictor import Predictor
import allennlp_models.rc

class PythonPredictor:
    def __init__(self):
        self.predictor = Predictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/bidaf-elmo-model-2020.03.19.tar.gz")

    def predict(self, passage, question):
        prediction = self.predictor.predict(
            passage=passage, question=question
        )

        return {'answer': prediction["best_span_str"]}