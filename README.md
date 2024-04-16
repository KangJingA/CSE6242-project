# CSE6242 project: Visualizing Singapore’s Public Bus Network

In this project, we integrated bus data from the Land Transport Authority of Singapore's [datamall](https://datamall.lta.gov.sg/content/datamall/en.html) to create a vizualization tool. The application allows the user to explore CO2 emissions from Singapore public buses, and compare the total emissions reduced.

The deployed application can be found here: [https://cse6242-project.onrender.com/](https://cse6242-project.onrender.com/)

## Getting started

### Prerequisites

Access to LTA's datamall requires an api key. You may request for one here: [request for api key](https://datamall.lta.gov.sg/content/datamall/en/request-for-api.html)

### Installation

1. Clone the repository
```
git clone https://github.com/KangJingA/CSE6242-project
```

2. Set up virtual environment
```
[CSE6242-PROJECT]$ python3.7 -m venv venv
```

3. Activate virtual environment
```
[CSE6242-PROJECT]$ . venv/bin/activate
```

4. Install all dependencies
```
[CSE6242-PROJECT]$ pip install -r requirements.txt
```

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
