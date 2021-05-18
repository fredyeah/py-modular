import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from py_modular.generative.utils import generate_grains, create_grains, interpolate_grains, save_grain_cloud

grains = create_grains(file_name='debussy_printemp.wav', file_location='', number_of_grains=2, checkpoint='wavenet-ckpt/model.ckpt-200000')
# grains = encode_grains(grains, 'model.ckpt-200000')     http://download.magenta.tensorflow.org/models/nsynth/wavenet-ckpt/model.ckpt-200000.tar
grains = interpolate_grains(grains, number_of_grains=128)
grains = generate_grains(grains, 'wavenet-ckpt/model.ckpt-200000')
save_grain_cloud(grains)
