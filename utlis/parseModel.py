import yaml
import larq as lq
import tensorflow as tf

class dumpModel:

    def __init__(self, model, ):
        '''
        DocString:  Constructor of class parseModel. Responsible for parsing larq/keras sequential models.
        '''
        self.model = model
        self.parseModel()
    
    def parseLayerName(self, layer):
        if "quant_conv2d" in layer.name:
            return "quant_conv2d"
        elif "batch_normalization" in layer.name:
            return "batch_normalization"
        elif "flatten" in layer.name:
            return "flatten"
        elif "quant_dense" in layer.name:
            return "quant_dense"
        else:
            raise AssertionError("%s layer is not supported yet."%(layer.name))
    
    def parseLayerAttributes(self, layer, op_type):
        attr_dict = []
        if op_type == "quant_conv2d":
            data = {}
            data['name'] = 'kernel_shape'
            data['data'] = list(layer.kernel_size)
            attr_dict.append(data)

            data = {}
            data['name'] = 'strides'
            data['data'] = list(layer.strides)
            attr_dict.append(data)

            data = {}
            data['name'] = 'activation'
            if(layer.activation.__name__ == 'linear'):
                data['data'] = 0
            attr_dict.append(data)
            
            assert(layer.activation.__name__ == 'linear')
        
        elif op_type == "batch_normalization":
            data = {}
            data['name'] = 'momentum'
            data['data'] = layer.momentum
            attr_dict.append(data)
        
        elif op_type == "flatten":
            pass

        elif op_type == "quant_dense":
            data = {}
            data['name'] = 'units'
            data['data'] = layer.units
            attr_dict.append(data)
            
            data = {}
            data['name'] = 'activation'
            if(layer.activation.__name__ == 'linear'):
                data['data'] = 0
            attr_dict.append(data)
            
            assert(layer.activation.__name__ == 'linear')
        
        else:
            raise ValueError("%s layer attributes not defined."%(op_type))
        return attr_dict
    
    def parseModel(self):
        self.arch = {}
        self.layers = []

        if(len(self.model.layers) == 0):
            raise AssertionError("The model doesn't have any layers to parse.")
        
        '''
        Parse Model input shape
        '''
        graph_input_shape = []
        for shape in self.model.input_shape:
            if shape is None:
                graph_input_shape.append(1)
            else:
                graph_input_shape.append(shape)
        self.arch['input_shape'] = {}
        self.arch['input_shape']['shape'] = graph_input_shape
        self.arch['input_shape']['dims'] = len(graph_input_shape)
        self.arch['input_shape']['name'] = 'input_0'

        for layer in self.model.layers:
            layer_dict = {}
            op_name = self.parseLayerName(layer)
            attributes = self.parseLayerAttributes(layer, op_name)
            layer_dict["op_name"] = op_name
            layer_dict['attributes'] = attributes
            self.layers.append(layer_dict)
        
        self.arch['layers'] = self.layers
    
    def dumpArch(self, out_path):
        fileHandler = open(out_path + "/arch.yml", 'w')
        yaml.dump(self.arch, fileHandler)


if __name__ == "__main__":

    qNet = tf.keras.Sequential()
    qNet = tf.keras.Sequential()
    qNet.add(lq.layers.QuantConv2D(128, kernel_size=8, strides=4, input_shape=(80, 80, 4), kernel_quantizer='ste_sign', kernel_constraint='weight_clip'))
    qNet.add(tf.keras.layers.BatchNormalization(momentum=0.999))
    qNet.add(lq.layers.QuantConv2D(256, kernel_size=4, strides=2, input_quantizer='ste_sign', kernel_quantizer='ste_sign', kernel_constraint='weight_clip'))
    qNet.add(tf.keras.layers.BatchNormalization(momentum=0.999))
    qNet.add(lq.layers.QuantConv2D(512, kernel_size=3, strides=1, input_quantizer='ste_sign', kernel_quantizer='ste_sign', kernel_constraint='weight_clip'))
    qNet.add(tf.keras.layers.BatchNormalization(momentum=0.999))
    qNet.add(tf.keras.layers.Flatten())
    qNet.add(lq.layers.QuantDense(512, input_quantizer='ste_sign', kernel_quantizer='ste_sign', kernel_constraint='weight_clip'))
    qNet.add(tf.keras.layers.BatchNormalization(momentum=0.999))
    qNet.add(lq.layers.QuantDense(3, input_quantizer='ste_sign', kernel_quantizer='ste_sign', kernel_constraint='weight_clip'))

    parser = dumpModel(qNet)
    parser.dumpArch("out/")