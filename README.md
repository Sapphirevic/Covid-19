# Covid-19
Data Visualization using dash plotly

## Project Setup

### Create a Virtual Environment
Setup a local environment using: 
```bash
python -m venv env
```

### Activate the Virtual Environment

On Windows run: 
```bash
env\\Scripts\\activate
```

On macOS/Linux run: 
```bash
source env/bin/activate
```

## Important!

For dependency updates, please run the following command whenever a new dependency is added:
```bash
pip freeze > requirements.txt
```
This will update the \`requirements.txt\` for easy setup in a different working environment.

Dependencies have been included in \`requirements.txt\`. Install them using:
```bash
pip install -r requirements.txt
```

### Run the project
First: 
```bash
cd Dash-Plotly
```

Run:
```bash
python covid.py
```