from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import requests

def print_welcome():
    print('Welcome to Airflow.')

def print_date():
    print(f'Today is {datetime.today().date()}')

def print_random_quote():
    response = requests.get('https://zenquotes.io/api/random')
    quote = response.json()[0]['q']
    print(f'Quote of the day: {quote}')

dag = DAG(
    'welcome_dag',
    default_args = {'start_date': days_ago(1)},
    schedule_interval = '1 * * * *',
    catchup = False
)

print_welcome_task = PythonOperator(
    task_id = 'print_welcome',
    python_callable = print_welcome,
    dag = dag
)

print_date_task = PythonOperator(
    task_id = 'print_date',
    python_callable = print_date,
    dag = dag
)

print_random_quote_task = PythonOperator(
    task_id = 'print_random_quote',
    python_callable = print_random_quote,
    dag = dag
)

# Task dependencies
print_welcome_task >> print_date_task >> print_random_quote_task