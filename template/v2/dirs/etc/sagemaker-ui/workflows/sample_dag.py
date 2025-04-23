from airflow.decorators import dag
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
}


@dag(default_args=default_args, tags=["sample"])
def sample_dag():
    def sample_task():
        _task = BashOperator(task_id="hello_world", bash_command="echo 'hello world!'")
        return _task

    task = sample_task()


sample_dag = sample_dag()
