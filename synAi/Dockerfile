FROM python:3.8
ADD finder.py .
ENV config_name='stress_pod_memory.yml'
ENV start_memory_value=200
ENV step_memory = "100"
ENV start_cpu_value = "2"
ENV step_cpu = "0"
ENV wait_time = "60"
ENV start=1


RUN pip install pyyaml
RUN pip install kubernetes
CMD python ./finder.py --config_name $config_name --start_memory_value $start_memory_value --start $start

