# Installation

**Note:** If you encounter any trouble with the installation, please refer to `README-WILDS` for a detailed installation process, as it outlines all dependencies.

To install the dependencies automatically, use:

```bash
pip install wilds
```

Running `pip install wilds` will automatically check for and install all required dependencies, except for `torch-scatter` and `torch-geometric` packages. These require manual installation. For more information, visit: [PyTorch Geometric Installation](https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html#installation-via-binaries).

To install `py150`, ensure you are in the topmost level of the repository (`path/to/wilds`) and execute:

```bash
python wilds/download_datasets.py --datasets py150 --root_dir data
```

# Setup

In our paper, we mention the datasets `data24k` and `data1500`, which are subsets of `py150` containing 24,000 and 1,500 training samples, respectively, instead of approximately 80,000 as in `py150`. This sampling decision was made due to the long runtime of training the full set. However, the ratios between the validation and testing data have been kept consistent in both subsets relative to `py150`.

To sample these subsets or others, ensure you are in the topmost level of the repository (`path/to/wilds`) and run with appropriate arguments:

```bash
python augmentation/sample_data.py --input data --output data24k --sample_size 24000

python augmentation/sample_data.py --input data --output data1500 --sample_size 1500
```

For clarity on command line arguments, run:

```bash
python augmentation/sample_data.py -h
```

**Note:** If you wish to run the augmentations on the full `py150`, you can skip the Setup section.

# Processing the Sampled Dataset

After sampling your dataset, it needs to be processed. Follow these steps:

**Step 0:** Navigate to the directory of the sampled set:

```bash
cd path/to/wilds/data1500/py150_v1.0/
```

**Step 1:** Run the tokenization script:

```bash
python script/1.prepare_tokenized.py
```

**Step 2:** Run the evaluation preparation script:

```bash
python script/2.prepare_eval_position.py
```

# Augmentations

We provide two different augmentation strategies: 'mixed' and 'combined'. The difference between these is explained in Section 4.2 of our paper (url: ...).

## Mixed Strategy

To run the augmentations with the 'mixed' strategy, ensure you are in the topmost level of the repository (`path/to/wilds`) and execute:

```bash
python augmentation/augment_mixed_file.py --data_dir data24k --aug_dir data24k-aug -s 24000 -k 1 logs/logs24k/mixed/all-1

python augmentation/augment_mixed_file.py --data_dir data1500 --aug_dir data1500-aug -s 1500 -k 1 logs/logs1500/mixed/all-1
```

For clarification on command line arguments, run:

```bash
python augmentation/augment_mixed_file.py -h
```

## Combined Strategy

To run the augmentations with the 'combined' strategy, ensure you are in the topmost level of the repository (`path/to/wilds`) and execute:

```bash
python augmentation/augment_combined_file.py --data_dir data24k --aug_dir data24k-aug -s 24000 -k 1 logs/logs24k/combined/all-1

python augmentation/augment_combined_file.py --data_dir data1500 --aug_dir data1500-aug -s 1500 -k 1 logs/logs1500/combined/all-1
```

For clarification on command line arguments, run:

```bash
python augmentation/augment_combined_file.py -h
```

The `logs` directory (or any directory of your choice) will store the `aug.log` file, indicating how many times each augmentation has been applied to the dataset, as well as the total number of augmentations. This content will also be printed on the terminal, indicating a successful execution of the script.

**Note:** Both `augment_mixed_file.py` and `augment_combined_file.py` implement what we call in the paper the 'enhanced augmentation set'. To exclude certain augmentations, please edit the script you wish to run by removing or commenting out the undesired refactorings from the `refactors_list` at the top of the script.

# Processing the Augmented Dataset

After augmenting your dataset, it needs to be processed before running on the model. Follow these steps:

**Step 0:** Navigate to the directory of the augmented set:

```bash
cd path/to/wilds/data1500-aug/py150_v1.0/
```

**Step 1:** Run the tokenization script:

```bash
python script/1.prepare_tokenized.py
```

**Step 2:** Run the evaluation preparation script:

```bash
python script/2.prepare_eval_position.py
```

# Running the Experiment

## Running the Sampled Control Dataset

Now, you are ready to run the control dataset. Ensure you are in the topmost level of the repository (`path/to/wilds`) and execute:

```bash
python examples/run_expt.py --root_dir data24k --log_dir logs/logs24k/control --dataset py150 --algorithm ERM --seed 0 --lr 8e-5 --weight_decay 0

python examples/run_expt.py --root_dir data1500 --log_dir logs/logs1500/control --dataset py150 --algorithm ERM --seed 0 --lr 8e-5 --weight_decay 0
```

Once `run_expt.py` has finished running, your results will be stored in the specified `log_dir`, within a file named `log.txt`. The results will also be printed on the terminal, indicating successful completion. 

For clarification on command line arguments, run:

```bash
python examples/run_expt.py -h
```

## Running the Augmented Dataset

Now, you are ready to run the augmented dataset. Ensure you are in the topmost level of the repository (`path/to/wilds`) and execute:

```bash
python examples/run_expt.py --root_dir data24k-aug --log_dir logs/logs24k/mixed/all-1 --dataset py150 --algorithm ERM --seed 0 --lr 8e-5 --weight_decay 0

python examples/run_expt.py --root_dir data1500-aug --log_dir logs/logs1500/combined/all-1 --dataset py150 --algorithm ERM --seed 0 --lr 8e-5 --weight_decay 0
```

Once `run_expt.py` has finished running, your results will be stored in the specified `log_dir`, within a file named `log.txt`. The results will also be printed on the terminal, indicating successful completion. 

For clarification on command line arguments, run:

```bash
python examples/run_expt.py -h
```
