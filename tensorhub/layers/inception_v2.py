# Copyright 2019 The TensorHub Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Load packages
from tensorflow import keras
from tensorhub.utilities.activations import relu


class BasicLayer(keras.layers.Layer):
    """Standard Inception V2 layer implemented as a keras layer for feature creation."""

    def __init__(self, num_filters=28, activation=relu, name=None):
        """Class constructor to initialize variables.

        Keyword Arguments:
            num_filters {int} -- Number of filters for convolution. (default: {28})
            activation {str} -- Activation to be applied on each convolution. (default: {"relu"})
            name {str} -- Name associated with this layer. (default: {None})
        """
        if name:
            super(BasicLayer, self).__init__(name=name)
        else:
            super(BasicLayer, self).__init__()
        self.num_filters = num_filters
        self.act = activation
        self.strides = 1
        self.padding = "same"

    def build(self, input_shape):
        """Lazing building of a layer.

        Arguments:
            input_shape {tensor} -- Input shape tensor.
        """
        self.conv_1a = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides * self.strides, padding=self.padding)
        self.conv_1b = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_3b = keras.layers.Conv2D(self.num_filters, (3, 3), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_1c = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_3c1 = keras.layers.Conv2D(self.num_filters, (3, 3), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_3c2 = keras.layers.Conv2D(self.num_filters, (3, 3), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_1d = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.maxpool_layer = keras.layers.MaxPool2D(pool_size=(3, 3), strides=self.strides, padding=self.padding)
        self.concat_layer = keras.layers.concatenate(axis=-1)

    def call(self, x):
        """Forward pass of the layer.

        Arguments:
            x {tensor} -- Input tensor to the layer.

        Returns:
            tensor -- Output tensor from the layer.
        """
        # Block 1
        out_a = self.conv_1a(x)
        # Block 2
        out_b_inter = self.conv_1b(x)
        out_b = self.conv_3b(out_b_inter)
        # Block 3
        out_c_inter = self.conv_1c(x)
        out_c_inter = self.conv_3c1(out_c_inter)
        out_c = self.conv_3c2(out_c_inter)
        # Block 4
        out_d_inter = self.maxpool_layer(x)
        out_d = self.conv_1d(out_d_inter)
        # Combine results from each block
        output = self.concat_layer([out_a, out_b, out_c, out_d], axis=-1)
        return output


class DeepLayer(keras.layers.Layer):
    """Deep Inception V2 layer implemeted as a kaeras layer for feature creation."""

    def __init__(self, num_filters=28, activation=relu, name=None):
        """Class constructor to initialize variables.

        Keyword Arguments:
            num_filters {int} -- Number of filters for convolution. (default: {28})
            activation {str} -- Activation to be applied on each convolution. (default: {"relu"})
            name {str} -- Name associated with this layer. (default: {None})
        """
        if name:
            super(DeepLayer, self).__init__(name=name)
        else:
            super(DeepLayer, self).__init__()
        self.num_filters = num_filters
        self.act = activation
        self.strides = 1
        self.padding = "same"

    def build(self, input_shape):
        """Lazing building of a layer.

        Arguments:
            input_shape {tensor} -- Input shape tensor.
        """
        self.conv_1a = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides * self.strides, padding=self.padding)
        self.conv_1b = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_1_3b = keras.layers.Conv2D(self.num_filters, (1, 3), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_3_1b = keras.layers.Conv2D(self.num_filters, (3, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_1c = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_1_3c1 = keras.layers.Conv2D(self.num_filters, (1, 3), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_3_1c1 = keras.layers.Conv2D(self.num_filters, (3, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_1_3c2 = keras.layers.Conv2D(self.num_filters, (1, 3), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_3_1c2 = keras.layers.Conv2D(self.num_filters, (3, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_1d = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.maxpool_layer = keras.layers.MaxPool2D(pool_size=(3, 3), strides=self.strides, padding=self.padding)

    def call(self, x):
        """Forward pass of the layer.

        Arguments:
            x {tensor} -- Input tensor to the layer.

        Returns:
            tensor -- Output tensor from the layer.
        """
        # Block 1
        out_a = self.conv_1a(x)
        # Block 2
        out_b_inter = self.conv_1b(x)
        out_b_inter = self.conv_1_3b(out_b_inter)
        out_b = self.conv_3_1b(out_b_inter)
        # Block 3
        out_c_inter = self.conv_1c(x)
        out_c_inter = self.conv_1_3c1(out_c_inter)
        out_c_inter = self.conv_3_1c1(out_c_inter)
        out_c_inter = self.conv_1_3c2(out_c_inter)
        out_c = self.conv_3_1c2(out_c_inter)
        # Block 4
        out_d_inter = self.maxpool_layer(x)
        out_d = self.conv_1d(out_d_inter)
        # Combine results from each block
        output = keras.layers.concatenate([out_a, out_b, out_c, out_d], axis=-1)
        return output


class WideLayer(keras.layers.Layer):
    """Wide Inception V2 layer implemented as a keras layer for feature creation."""

    def __init__(self, num_filters=28, activation=relu, name=None):
        """Class constructor to initialize variables.

        Keyword Arguments:
            num_filters {int} -- Number of filters for convolution. (default: {28})
            activation {str} -- Activation to be applied on each convolution. (default: {"relu"})
            name {str} -- Name associated with this layer. (default: {None})
        """
        if name:
            super(WideLayer, self).__init__(name=name)
        else:
            super(WideLayer, self).__init__()
        self.num_filters = num_filters
        self.act = activation
        self.strides = 1
        self.padding = "same"

    def build(self, input_shape):
        """Lazing building of a layer.

        Arguments:
            input_shape {tensor} -- Input shape tensor.
        """
        self.conv_1a = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides * self.strides, padding=self.padding)
        self.conv_1b = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_1_3b = keras.layers.Conv2D(self.num_filters, (1, 3), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_3_1b = keras.layers.Conv2D(self.num_filters, (3, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_1c = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_3c = keras.layers.Conv2D(self.num_filters, (3, 3), activation=self.act,strides=self.strides, padding=self.padding)
        self.conv_1_3c = keras.layers.Conv2D(self.num_filters, (1, 3), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_3_1c = keras.layers.Conv2D(self.num_filters, (3, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.conv_1d = keras.layers.Conv2D(self.num_filters, (1, 1), activation=self.act, strides=self.strides, padding=self.padding)
        self.maxpool_layer = keras.layers.MaxPool2D(pool_size=(3, 3), strides=self.strides, padding=self.padding)
        self.concat_layer = keras.layers.concatenate(axis=-1)

    def call(self, x):
        """Forward pass of the layer.

        Arguments:
            x {tensor} -- Input tensor to the layer.

        Returns:
            tensor -- Output tensor from the layer.
        """
        # Block 1
        out_a = self.conv_1a(x)
        # Block 2
        out_b_inter = self.conv_1b(x)
        out_b1 = self.conv_1_3b(out_b_inter)
        out_b2 = self.conv_3_1b(out_b_inter)
        # Block 3
        out_c_inter = self.conv_1c(x)
        out_c_inter = self.conv_3c(out_c_inter)
        out_c1 = self.conv_1_3c(out_c_inter)
        out_c2 = self.conv_3_1c(out_c_inter)
        # Block 4
        out_d_inter = self.maxpool_layer(x)
        out_d = self.conv_1d(out_d_inter)
        # Combine results from each block
        output = self.concat_layer([out_a, out_b1, out_b2, out_c1, out_c1, out_d], axis=-1)
        return output