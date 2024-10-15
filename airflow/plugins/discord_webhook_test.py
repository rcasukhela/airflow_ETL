from airflow.models import Variable
from airflow.models.taskinstance import TaskInstance
from airflow.models.dagrun import DagRun
from discord_webhook import DiscordWebhook, DiscordEmbed

def discord_webhook_0(**kwargs):
    
    ti : TaskInstance=kwargs['ti']
    ts = kwargs['ts']
    ds = kwargs['ds']
    dag = kwargs['dag']
    webhook = DiscordWebhook(url=Variable.get("discord_webhook_0")) # Update variable name with your change
    embed = DiscordEmbed(title="Airflow Alert - Task has failed!", color='CC0000')
    # embed.add_embed_field(name="DAG", value=dag_run.dag_id, inline=True)
    # embed.add_embed_field(name="PRIORITY", value="HIGH", inline=True)
    # embed.add_embed_field(name="TASK", value=context.task_instance, inline=False)
    # embed.add_embed_field(name="ERROR", value='error')
    embed.add_embed_field(name='DAG DETAILS', value=f'{ti}, {ts}, {ds}, {dag}')
    webhook.add_embed(embed)
    response = webhook.execute()

def send_alert_discord(**kwargs):
	# Get Task Instances variables
	last_task = kwargs['ti']
	task_name = last_task.task_id
	dag_name = last_task.dag_id
	log_link = last_task.log_url
	execution_date = str(kwargs['logical_date'])

	# Extract reason for the exception
	try:
		error_message = str(kwargs["exception"])
	except:
		error_message = "Some error that cannot be extracted has occurred. Visit the logs!"

	# Send Alert
	webhook = DiscordWebhook(url=Variable.get("discord_webhook_0")) # Update variable name with your change
	embed = DiscordEmbed(title="Airflow Alert - Task has failed!", color='CC0000')
	embed.add_embed_field(name="DAG", value=dag_name, inline=True)
	embed.add_embed_field(name="PRIORITY", value="HIGH", inline=True)
	embed.add_embed_field(name="TASK", value=task_name, inline=False)
	embed.add_embed_field(name="ERROR", value=error_message)
	webhook.add_embed(embed)
	response = webhook.execute()

	return response