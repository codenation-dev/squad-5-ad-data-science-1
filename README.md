# Final Project Squad5
The goal of this product is to provide an automated service that recommends new leads to a given user based on their current list of customers (Portfolio).

## Stakeholders
We are the Squad5 of the **AceleraDev Data Science 2019** acceleration course.

| Role                 | Responsibility         | Full name                |
| -----                | ----------------       | -----------              |
| Data Scientist       | Author                 | [`Igor Lucena Peixoto Andrezza`] |
| Data Scientist       | Author                 | [`Octávio Santana`] |
| Data Scientist       | Author                 | [`Pedro Bueno de Almeida`] |

## Usage
See how simple that is to use this service.


**1.** Clone this repository:
```
git clone https://github.com/codenation-dev/squad-5-ad-data-science-1.git
```

**2.** Download [market data](https://www.kaggle.com/argonalyst/aceleradev-ds-final-project-2019) and place it inside:
```
/workspace/data
```

**3.** Navigate to project folder:
```
cd final_project_squad5
```

**4.** Install requirements.txt:
```
pip install -r requirements.txt
```

**5.** Run using an example portfolio:
```
python main.py run
```

**6.** Or run using your own portfolio (See [specifications](./docs/portfolio_specification.md)):
```
python main.py run --portfolio "csv_with_companies_ids.csv"
```

New **recommended leads** are stored at `recommendations.txt`

You can check the perfomance metrics of your *run* on `performance.json`

Check this [Jupyter Notebook](https://github.com/codenation-dev/squad-5-ad-data-science-1/blob/master/analysis/Projeto%20Final%20-%20Squad5%20-%20v1.ipynb) for a deep explanation about what is happening under the hood. 
