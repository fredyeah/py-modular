import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from py_modular.generative.utils import generate_grains, create_grains, interpolate_grains

grains = create_grains(file_name='some_wav_file.wav', file_location='', number_of_grains=2)
grains = encode_grains(grains, 'model.ckpt-200000')
grains = interpolate_grains(grains, number_of_grains=128)
grains = generate_grains(grains, 'model.ckpt-200000')
save_grain_cloud(grains)
