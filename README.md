# AlphafoldInstallation
<img src="https://img.shields.io/badge/Platform-Ubuntu-brightgreen" />
<img src=https://img.shields.io/badge/AlphaFold-v2.3.2-blue/>

## Background
As the hottest AI in biology, AlphaFlod2 has brought epochal influence to the biomedical field, and many researchers have begun to try to bring AlphaFold2 into their own work.
However, alphafold relies not only on a lot of bioinformatics software, but also on a lot of Python-related packages, the installation process is not very friendly to biological and non-biological researchers. Therefore, the aim of this project is to help researchers "One-click use of AlphaFold".

## Features
- [x] Automatically installs alphafold's dependent softwares
- [x] Automatically installs alphafold's dependent python packages
- [x] Part of the alphafold code is automatically modified to match the last version of OpenMM

## TODO
- [ ] Automatically download the database required for alphafold
- [ ] Program error detection
- [ ] Demo run test module
## Start

### Install
```
wget https://github.com/LoveFishoO/AlphafoldInstallation/archive/refs/tags/<version>.tar.gz
tar -zxvf ./AlphafoldInstallation-<version>
```
### Usage
```
cd ./AlphafoldInstallation-<version>
python alphafold_install.py

# download database
./alphafold/scripts/download_all_data.sh <DOWNLOAD_DIR> > download.log 2> download_all.log &

# Run
python ./alphafold/run_alphafold.py \
    --fasta_paths=rcsb_pdb_4D2I.fasta \
    --max_template_date=2020-05-14 \
    --model_preset=monomer \  
    --db_preset=full_dbs \ 
    --data_dir=<DOWNLOAD_DIR> \
    --output_dir=./output/ \
    --uniref90_database_path=<DOWNLOAD_DIR>/uniref90/uniref90.fasta \
    --mgnify_database_path=<DOWNLOAD_DIR>/mgnify/mgy_clusters_2022_05.fa \
    --template_mmcif_dir=<DOWNLOAD_DIR>/pdb_mmcif/mmcif_files/ \
    --obsolete_pdbs_path=<DOWNLOAD_DIR>/pdb_mmcif/obsolete.dat \
    --use_gpu_relax=False \
    --bfd_database_path=<DOWNLOAD_DIR>/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
    --uniref30_database_path=<DOWNLOAD_DIR>/uniref30/UniRef30_2021_03 \
    --pdb70_database_path=<DOWNLOAD_DIR>/pdb70/pdb70

```

## Related Efforts
[Chinese tutorial](https://blog.csdn.net/qq_39415941/article/details/128919047#comments_26199296)

## Maintainers
[@LoveFish](https://github.com/LoveFishoO)

## Contributing
Feel free to dive in! Open an issue or submit PRs.

### Contributors
[@LoveFish](https://github.com/LoveFishoO)

## Backers
Thank you to all my backers! 🙏<br><br>
<img src="https://raw.githubusercontent.com/LoveFishoO/AlphafoldInstallation/main/imgs/Tina.jpg" width="50" height="50" alt="Tina Hu" title="Tina Hu"/><br/> <b>Tina Hu</b>