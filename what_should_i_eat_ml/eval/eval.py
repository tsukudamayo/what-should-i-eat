import transformers
transformers.BertTokenizer = transformers.BertJapaneseTokenizer
from sentence_transformers import SentenceTransformer
from sentence_transformers import models
from sentence_transformers.losses import TripletDistanceMetric, TripletLoss
from sentence_transformers.evaluation import TripletEvaluator
from sentence_transformers.readers import TripletReader
from sentence_transformers.datasets import SentencesDataset


class SentenceEmbeddingsHandler(BaseHandler):
    """
    The handler takes an input string and returns the classification text 
    based on the serialized transformers checkpoint.
    """
    def __init__(self):
        super(SentenceEmbeddingsHandler, self).__init__()
        self.initialized = False

    def initialize(self, ctx):
        """ Loads the model.pt file and initializes the model object.
        Instantiates Tokenizer for preprocessor to use
        Loads labels to name mapping file for post-processing inference response
        """
        self.manifest = ctx.manifest

        properties = ctx.system_properties
        model_dir = properties.get("model_dir")
        self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

        # Read model serialize/pt file
        serialized_file = self.manifest["model"]["serializedFile"]
        model_pt_path = os.path.join(model_dir, serialized_file)
        if not os.path.isfile(model_pt_path):
            raise RuntimeError("Missing the model.pt or pytorch_model.bin file")
        
        # Load model
        self.model = SentenceTransformer("sbert/")
        logger.debug('Transformer model from path {0} loaded successfully'.format(model_dir))
        
        # Ensure to use the same tokenizer used during training
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')
        else:
            logger.warning('Missing the index_to_name.json file. Inference output will not include class name.')

        self.initialized = True
 def preprocess(self, data):
        """ Preprocessing input request by tokenizing
            Extend with your own preprocessing steps as needed
        """
        text = data[0].get("data")
        if text is None:
            text = data[0].get("body")
        sentences = text.decode('utf-8')
        logger.info("Received text: '%s'", sentences)

        return sentences

    def inference(self, inputs):
        """ Predict the class of a text using a trained transformer model.
        """
        prediction = self.model.encode(inputs)

        logger.info("Model predicted: '%s'", prediction)
        return [prediction]

    def postprocess(self, inference_output):
        return inference_output
