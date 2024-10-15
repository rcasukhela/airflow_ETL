import re
import logging

from airflow import DAG
from airflow.models import Variable, TaskInstance
from airflow.operators.python_operator import PythonOperator
from airflow.utils.email import send_email

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests

TI = TaskInstance

def print_random_quote():
    response = requests.get('https://zenquotes.io/api/random')
    quote = response.json()[0]['q']
    print(f'Quote of the day: {quote}')
    1 / 0

def send_alert_discord(context):
	# Get Task Instances variables
    try:
        ti = context['ti']
        ts = context['ts']
        ds = context['ds']
        dag = context['dag']
        error = context['exception']
        logging.info(f"Sending Discord alert for failed task: {ti.task_id}")
        webhook = DiscordWebhook(url=Variable.get("discord_webhook_0"))
        embed = DiscordEmbed(title=f"Airflow  - task {error}!", color='CC0000')
        embed.add_embed_field(name='DAG DETAILS', value=f'{ti}, {ts}, {ds}, {dag}, {error}')
        webhook.add_embed(embed)
        response = webhook.execute()
        logging.info(f"Discord webhook response: {response}")
    except Exception as e:
        logging.error(f"Failed to send Discord alert: {e}")


default_args = {
	'owner': 'airflow',
	'start_date': datetime.strptime("2022-04-11 20:00:00", "%Y-%m-%d %H:%M:%S"),
	'end_date': None,
	'retries': 0,
	'retry_delay': timedelta(minutes=0),
	'on_failure_callback': send_alert_discord,
    'on_success_callback': send_alert_discord,
    'on_execute_callback': send_alert_discord, # Update alert function name with your change.
}

dag = DAG(
	'AAA_discord_webhook_on_failure_test', 
	default_args=default_args,
    schedule_interval = None,
	concurrency=16, 
	max_active_runs=16
)

print_random_quote_task = PythonOperator(
    task_id = 'print_random_quote',
    python_callable = print_random_quote,
    provide_context=True,
    dag = dag
)

print_random_quote_task