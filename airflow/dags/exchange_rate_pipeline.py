from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from clean_data import clean_data

# Define the DAG
dag = DAG(
    'exchange_rate_etl',
    start_date=datetime(2024, 10, 1),
    schedule_interval = '0 22 * * *',
    default_args = {'retries': 2, 'retry_delay': timedelta(seconds=1)},
    catchup=False
)

# Define tasks
download_task = BashOperator(
    task_id='download_file',
    bash_command="curl -o xrate.csv {{ var.value.get('web_api_key')}}",
    cwd='/tmp',
    dag=dag
)

clean_data_task = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data,
    dag=dag
)

# send_email_task = EmailOperator(
#     task_id='send_email',
#     to='ydyiwadw@sharklasers.com',
#     subject='Exchange Rate Download successful',
#     html_content = 'The Exchange Rate data has been successfully downloaded, cleaned, and loaded.',
#     dag=dag
# )

# Define task dependencies
download_task >> clean_data_task # >> send_email_task