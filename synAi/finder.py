from os import path
import os
import time
import argparse
from kubernetes import client, config
import yaml


def find_limits_memory(config_name, start_value, step, sleep_time=60):
    config.load_kube_config()

    with open(path.join(path.dirname(__file__), config_name)) as f:
        dep = yaml.safe_load(f)
    k8s_apps_v1 = client.CoreV1Api()
    name = dep['metadata']['name']
    namespace = dep['metadata']['namespace']
    default = start_value

    dep['spec']['containers'][0]['resources']['limits']['memory'] = '{0}Mi'.format(default)
    dep['spec']['containers'][0]['resources']['requests']['memory'] = '{0}Mi'.format(default)
    k8s_apps_v1.create_namespaced_pod(body=dep, namespace=namespace)
    print('memory finder is sleeping')
    time.sleep(sleep_time)
    resp = k8s_apps_v1.read_namespaced_pod_status(name=name, namespace=namespace)
    answ = resp.to_dict()

    if (answ['status']['container_statuses'][0]['ready'] == True):
        flag = 1
        k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
        time.sleep(sleep_time)

    else:
        flag = -1
        k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
        time.sleep(sleep_time)

    if(flag == 1):
        while (True):
            default_old = default
            default -= step
            dep['spec']['containers'][0]['resources']['limits']['memory'] = '{0}Mi'.format(default)
            dep['spec']['containers'][0]['resources']['requests']['memory'] = '{0}Mi'.format(default)

            k8s_apps_v1.create_namespaced_pod(body=dep, namespace=namespace)
            print('memory finder is sleeping')
            time.sleep(sleep_time)
            resp = k8s_apps_v1.read_namespaced_pod_status(name=name, namespace=namespace)
            answ = resp.to_dict()
            if (answ['status']['container_statuses'][0]['ready'] == False):
                k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
                time.sleep(sleep_time)
                return default_old
            else:
                k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
                time.sleep(sleep_time)
    else:
        while (True):
            default += step
            dep['spec']['containers'][0]['resources']['limits']['memory'] = '{0}Mi'.format(default)
            dep['spec']['containers'][0]['resources']['requests']['memory'] = '{0}Mi'.format(default)

            k8s_apps_v1.create_namespaced_pod(body=dep, namespace=namespace)
            print('memory finder is sleeping')
            time.sleep(sleep_time)
            resp = k8s_apps_v1.read_namespaced_pod_status(name=name, namespace=namespace)
            answ = resp.to_dict()
            if (answ['status']['container_statuses'][0]['ready'] == True):
                k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
                time.sleep(sleep_time)
                return default
            else:
                k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
                time.sleep(sleep_time)


def find_request_cpu(config_name, start_value, step, sleep_time=60):
    config.load_kube_config()
    with open(path.join(path.dirname(__file__), config_name)) as f:
        dep = yaml.safe_load(f)
    k8s_apps_v1 = client.CoreV1Api()
    name = dep['metadata']['name']
    namespace = dep['metadata']['namespace']
    default = start_value

    dep['spec']['containers'][0]['resources']['limits']['cpu'] = '{0}'.format(default)
    dep['spec']['containers'][0]['resources']['requests']['cpu'] = '{0}'.format(default)
    k8s_apps_v1.create_namespaced_pod(body=dep, namespace=namespace)
    print('cpu finder is sleeping')
    time.sleep(sleep_time)
    resp = k8s_apps_v1.read_namespaced_pod_status(name=name, namespace=namespace)
    answ = resp.to_dict()

    if (answ['status']['container_statuses']!= None):
        flag = 1
        k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
        time.sleep(sleep_time)

    else:
        flag = -1
        k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
        time.sleep(sleep_time)

    if (flag == 1):
        while (True):
            default_old = default
            default += step
            dep['spec']['containers'][0]['resources']['limits']['cpu'] = '{0}'.format(default)
            dep['spec']['containers'][0]['resources']['requests']['cpu'] = '{0}'.format(default)

            k8s_apps_v1.create_namespaced_pod(body=dep, namespace=namespace)
            print('cpu finder is sleeping')
            time.sleep(sleep_time)
            resp = k8s_apps_v1.read_namespaced_pod_status(name=name, namespace=namespace)
            answ = resp.to_dict()
            if (answ['status']['container_statuses'] == None):
                k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
                time.sleep(sleep_time)
                return default_old
            else:
                k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
                time.sleep(sleep_time)
    else:
        while (True):
            default -= step
            dep['spec']['containers'][0]['resources']['limits']['cpu'] = '{0}'.format(default)
            dep['spec']['containers'][0]['resources']['requests']['cpu'] = '{0}'.format(default)

            k8s_apps_v1.create_namespaced_pod(body=dep, namespace=namespace)
            print('cpu finder is sleeping')
            time.sleep(sleep_time)
            resp = k8s_apps_v1.read_namespaced_pod_status(name=name, namespace=namespace)
            answ = resp.to_dict()
            if (answ['status']['container_statuses'] != None):
                k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
                time.sleep(sleep_time)
                return default
            else:
                k8s_apps_v1.delete_namespaced_pod(name=name, namespace=namespace)
                time.sleep(sleep_time)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config_name", type=str, help="name of the config file")
    parser.add_argument("--start_memory_value", type=str, help="start value of memory")
    parser.add_argument("--step_memory", type=str, help="step of memory")
    parser.add_argument("--start_cpu_value", type=str, help="start value of cpu")
    parser.add_argument("--step_cpu", type=str, help="step of cpu")
    parser.add_argument("--wait_time", type=str, help="wait time")
    parser.add_argument("--start", type=str, help="test")

    args = parser.parse_args()
    checker = int(args.start)
    PATH = "./etc/config/" + args.config_name
    print(PATH)
    config.load_incluster_config()

    with open(path.join(path.dirname(__file__), PATH)) as f:
        dep = yaml.safe_load(f)
    k8s_apps_v1 = client.CoreV1Api()
    k8s_apps_v1.list_pod_for_all_namespaces(watch=False)
    name = dep['metadata']['name']
    namespace = dep['metadata']['namespace']
    default = 300

    dep['spec']['containers'][0]['resources']['limits']['cpu'] = '{0}'.format(default)
    dep['spec']['containers'][0]['resources']['requests']['cpu'] = '{0}'.format(default)
    k8s_apps_v1.create_namespaced_pod(body=dep, namespace=namespace)


if __name__ == '__main__':
    main()


