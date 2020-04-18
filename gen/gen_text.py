import gpt_2_simple as gpt2
from datetime import datetime

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')

'''
gen = gpt2.generate(sess,
              length=200,
              temperature=0.85,
              nsamples=20,
              truncate='<|endoftext|>',
              prefix = "adam geldi ",
              include_prefix = False,
              batch_size = 2,
              return_as_list=True
              )
print(gen)
'''

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
                        batch_size=20
                        )