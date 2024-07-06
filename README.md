# Interpretable Dialect Classifier
This is the official repository for [Extracting Lexical Features from Dialects via Interpretable Dialect Classifiers ](https://arxiv.org/abs/2402.17914). We provide the code for training and evaluating the dialect classifiers, as well as the code for extracting and evaluating the lexical features. 

## Requirements
```pip install -r requirements.txt``` 

## Data
The data used in this work are the [FRMT](https://arxiv.org/abs/2210.00193), [LSDC](https://aclanthology.org/2020.vardial-1.3/), [ITDI](https://aclanthology.org/2022.vardial-1.13.pdf), and [Europarl v8](https://aclanthology.org/2005.mtsummit-papers.11/) datasets. The processed data and data processing scripts are placed in the `data` directory.

## Training
Both training code for LOO and selfExplain are placed in the `model` directory. 

## Evaluation
The evaluation code and data including `plasusibility`, `sufficiency`, and `human evaluation` are placed in the `evaluation` directory.

## Citation
If you use our tool, we'd appreciate if you cite the following paper:
```
@misc{xie2024extracting,
      title={Extracting Lexical Features from Dialects via Interpretable Dialect Classifiers}, 
      author={Roy Xie and Orevaoghene Ahia and Yulia Tsvetkov and Antonios Anastasopoulos},
      year={2024},
      eprint={2402.17914},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
