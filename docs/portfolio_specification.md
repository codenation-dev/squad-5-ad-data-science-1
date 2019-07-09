# Portfolio specification
> This document contains specifications about how your **personalized portfolio** should be.

This *Recommender System Model* was created for the **AceleraDev Data Science 2019** challenge. The challenge consisted on creating an algorithm able to find recomendations in the "market" using a portfolio as a base.

The "market" is represented by the file "estaticos_market.csv" located at `../workspace/data/` with 460k+ companies, containing multiple features. The "Portfolio" represents a subset of the "market", containing the Ids of companies which belongs to that portfolio.

## Using a personalized portfolio
> See how can you provide your own portfolio.

You can use your own subset of the "market" which will represents your portfolio, and needs to follow the **Portfolio structure** below.

## Portfolio structure
> The table below summarizes a portfolio structure.

|   | id |
|---|-----------------|
| 0 | 09e95c1a8404900 |
| 1 | dc9d155f5bcd317 |
| 2 | 16843c9ffb92017 |
| 3 | ff045934d90aab1 |

The function `rebuild_portfolio` inside `main.py` will recreate all the *features* for the personalized portfolio, so you only need to provide the companies Ids in a `.csv` file separated by commas.

## Usage
> How to use your own portfolio.

Navigate to the project's folder, install `requirements.txt` and execute the code below:

`python main.py run --portfolio "path/your_portfolio.csv"`

New recommendations and the performance metrics will be saved on the `output` folder.