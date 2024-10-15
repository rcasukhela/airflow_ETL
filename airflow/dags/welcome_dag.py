from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from discord_webhook_test import discord_webhook_0, send_alert_discord
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import requests

def print_welcome():
    print('Welcome to Airflow.')

def print_date():
    print(f'Today is {datetime.today().date()}')

def print_random_quote():
    response = requests.get('https://zenquotes.io/api/random')
    quote = response.json()[0]['q']
    print(f'Quote of the day: {quote}')


default_args = {
	'owner': 'airflow',
	'start_date': days_ago(1),
	'end_date': None,
	'retries': 0,
	'retry_delay': timedelta(minutes=0),
	'depends_on_past': False,
	'on_failure_callback': send_alert_discord # Update alert function name with your change.
}

dag = DAG(
    'welcome_dag',
    default_args = default_args,
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

send_discord_webhook_task = PythonOperator(
    task_id='send_discord_message',
    python_callable = discord_webhook_0,
    provide_context=True,
    dag = dag
)

# Task dependencies
print_welcome_task >> print_date_task >> print_random_quote_task >> send_discord_webhook_task