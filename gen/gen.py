# to bulk generate text locally using a trained model

import gpt_2_simple as gpt2
from datetime import datetime

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='r1')

num_files = 10

for _ in range(num_files):
    gen_file = 'gpt2_gentext_{:%Y%m%d_%H%M%S}.txt'.format(datetime.utcnow())

    gpt2.generate_to_file(sess,
                        destination_path=gen_file,
                        length=200,
                        temperature=0.85,
                        top_p=0.9,
                        prefix='<|startoftext|>',
                        truncate='<|endoftext|>',
                        include_prefix=False,
                        nsamples=1000,
                        batch_size=20)