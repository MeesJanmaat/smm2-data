## SMM2 data visualization

Contains the data and analysis scripts for the maker-player comparison in Super Mario Maker 2.
To run the `dump_object_counts.py` and `gen_misc_data.py` scripts, you need the [full dataset](https://huggingface.co/datasets/TheGreatRambler/mm2_level) downloaded in the directory of the repository. The visualization scripts will work without the dataset.

Dependencies:
 - `matplotlib 3.9.2`
 - `pandas 2.2.3`
 - `pillow 10.3.0`
 - `pickle 4.0`
Additional dependencies to reproduce data:
 - `kaitaistruct` and `mm2_level` from the [dataset repository](https://huggingface.co/datasets/TheGreatRambler/mm2_level)