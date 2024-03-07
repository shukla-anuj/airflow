import textwrap

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta,datetime

with DAG(
    "tutorial-firstdag-anuj",
    default_args={
        "depend_on_past":False,
        "email":["anujshukla4585@gmail.com"],
        "email_on_failure":False,
        "email_one_retry":False,
        "retries":1,
        "retry_delay": timedelta(minutes = 5)
    },
    description="first dag",
    schedule=timedelta(days=1),
    start_date=datetime(2024,3,7),
    catchup=False,
    tags=["first-dag"]
) as dag:
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date"
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3
    )

    templated_command = textwrap.dedent(
        """
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7) }}"
        {% endfor %}
        """
    )

    t3 = BashOperator(
        task_id="tmplated_id",
        depends_on_past=False,
        bash_command=templated_command
    )

    t1 >> [t2,t3]

