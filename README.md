# CSE6242 project: Visualizing Singapore’s Public Bus Network

In this project, we integrated bus data from the Land Transport Authority of Singapore's [datamall](https://datamall.lta.gov.sg/content/datamall/en.html) to create a vizualization tool. The application allows the user to explore CO2 emissions from Singapore public buses, and compare the total emissions reduced.

The deployed application can be found here: [https://cse6242-project.onrender.com/](https://cse6242-project.onrender.com/)

## Getting started

### Prerequisites

1. We suggest using python virtual envrionments. In this tutorial, `conda` is used.

2. Access to LTA's datamall requires an api key. You may request for one here: [request for api key](https://datamall.lta.gov.sg/content/datamall/en/request-for-api.html)

### Installation

1. Clone the repository and cd into the repository
```
git clone https://github.com/KangJingA/CSE6242-project
```

2. Set up virtual environment
```
[CSE6242-PROJECT]$ conda create --name venv
```

3. Activate virtual environment
```
[CSE6242-PROJECT]$ conda activate ./venv
```

4. Install all dependencies
```
[CSE6242-PROJECT]$ conda install --file requirements.txt
```

### Execution

5. Run Dash Application
```
[CSE6242-PROJECT]$ python ./Dash/app.py
```

6. View the application at http://127.0.0.1:8050/

### Preprocessing data 
Preprocessing data are done in the jupypter notebooks located in `/preprocess`.
To query data from LTA's datamall, an API key is required: [Prerequisites](#Prerequisites)

### Contributing
This project is a joint collaboration from group members from <b>team APAC<b>.
- Dahee choi
- Che Lee
- Nicholas Ang
- Phoebe Yuen
- Jessy Chen
