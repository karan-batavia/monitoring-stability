import csv 
import sys
import json


def main():

    print(sys.argv)
    stable_file = sys.argv[1]
    dev_file = sys.argv[2]

    filename = stable_file.split('/')[-1].split('.')[0]
    print(filename)
    previous_file = open(stable_file)
    current_file = open(dev_file)

    previous_data = json.load(previous_file)
    current_data = json.load(current_file)

    report = []
    repo_name = previous_data['repoName']


    report.append(['Base Version', '', '', '', 'Latest Version'])
    report.append(['privadoCoreVersion', previous_data['privadoCoreVersion'], '', '', 'privadoCoreVersion', current_data['privadoCoreVersion']])
    
    report.append(['privadoCLIVersion', previous_data['privadoCLIVersion'], '', '', 'privadoCLIVersion', current_data['privadoCLIVersion']])

    report.append(['privadoMainVersion', previous_data['privadoMainVersion'], '', '', 'privadoMainVersion', current_data['privadoMainVersion']])


    report.append([])
    report.append([])
    source_data_stable = previous_data['sources']
    source_data_dev = current_data['sources']
    
    report.append(['Analysis for sources'])
    for row in process_new_sources(source_data_stable, source_data_dev, repo_name):
        report.append(row)

    report.append([])
    report.append([])

    dataflow_stable = previous_data['dataFlow']
    dataflow_dev = current_data['dataFlow']

    report.append(['Analysis for Storages Sinks'])

    for row in process_sinks(dataflow_stable, dataflow_dev, repo_name,key='storages'):
        report.append(row)

    report.append([])
    report.append([])


    report.append(['Analysis for third_parties Sinks'])

    for row in process_sinks(dataflow_stable, dataflow_dev, repo_name,key='third_parties'):
        report.append(row)
    

    report.append([])
    report.append([])

    report.append(['Analysis for Leakages DataFlows'])

    for row in process_leakages(dataflow_stable, dataflow_dev, repo_name):
        report.append(row)

    report.append([])
    report.append([])

    create_csv(report, f'{filename}.csv')

    previous_file.close()
    current_file.close()

def process_sources_data(report, previous_data, current_data):
    report.append([])
    report.append([])

    report.append(['Sources Report'])

    report.append([])

    report.append(['Main Version', 'Current Version'])

    previous_count = 0
    current_count = 0

    for i in range(0, min(len(previous_data), len(current_data))):
        report.append([previous_data[previous_count]['id'], current_data[current_count]['id']])
        previous_count = previous_count + 1
        current_count = current_count + 1

    while previous_count < len(previous_data):
        report.append([previous_data[previous_count]['id']])
        previous_count = previous_count + 1

    while current_count < len(current_data):
        report.append(["", current_data[current_count]['id']])
        current_count = current_count + 1

def process_processing_data(report, previous_data, current_data):

    report.append([])
    report.append([])

    report.append(['Processing Report'])

    report.append([])

    report.append(['SourceId Name', 'Previous Count', 'Current Count'])

    previous_value = {}
    current_value = {}
    items = set()

    for i in previous_data:
        previous_value[i['sourceId']] = len(i['occurrences'])
        items.add(i['sourceId'])

    for i in current_data:
        current_value[i['sourceId']] = len(i['occurrences'])
        items.add(i['sourceId'])

    for i in items:
        count_a = previous_value[i] if i in previous_value else 0
        count_b = current_value[i] if i in current_value else 0
        report.append([i, count_a, count_b])

def process_collection(report, previous_data, current_data):


    report.append([])
    report.append([])

    report.append(['Collections Report'])

    report.append([])

    report.append(['SourceId Name', 'Previous Count', 'Current Count'])

    previous_value = {}
    current_value = {}
    items = set()

    for i in previous_data:
        previous_value[i['sourceId']] = len(i['occurrences'])
        items.add(i['sourceId'])
    
    for i in current_data:
        current_value[i['sourceId']] = len(i['occurrences'])
        items.add(i['sourceId'])

    for i in items:
        count_a = previous_value[i] if i in previous_value else 0
        count_b = current_value[i] if i in current_value else 0
        report.append([i, count_a, count_b])


def process_violations(report, previous_data, current_data):
    
    report.append([])
    report.append([])

    report.append(['Violations Report'])

    report.append([])

    report.append(['Main Version', 'Current Version'])

    previous_count = 0
    current_count = 0

    for i in range(0, min(len(previous_data), len(current_data))):
        report.append([previous_data[previous_count]['policyId'], current_data[current_count]['policyId']])
        previous_count = previous_count + 1
        current_count = current_count + 1

    while previous_count < len(previous_data):
        report.append([previous_data[previous_count]['policyId']])
        previous_count = previous_count + 1

    while current_count < len(current_data):
        report.append(["", current_data[current_count]['policyId']])
        current_count = current_count + 1

def create_csv(data, filename):

    with open(f'./{filename}.csv', "w") as value:
        report = csv.writer(value)
        for i in data:
            report.writerow(i)

    print("Report written")



def process_new_sources(source_stable, source_dev, repo_name):

    source_headings = ['repo_name', 'Number of Sources ( Base )', 'Number of Sources ( Latest )', 'List of Sources ( Base )', 'List of Sources ( Latest )', '% of change w.r.t base', 'New Sources added in Latest', 'Existing Sources remvoed from Latest']
    stable_sources = len(source_stable)
    dev_sources = len(source_dev)

    source_names_stable = '\n'.join(list(map(lambda x: x['name'], source_stable)))
    source_names_dev = '\n'.join(list(map(lambda x: x['name'], source_dev)))

    # percent change in latest sources wrt stable release
    percent_change = f'{((dev_sources - stable_sources) / stable_sources) * 100}%'   

    new_latest = '\n'.join(list(set(source_names_dev) - set(source_names_stable)))
    removed_dev = '\n'.join(list(set(source_names_stable) - set(source_names_dev)))

    result = [repo_name, stable_sources, dev_sources, source_names_stable, source_names_dev, percent_change, new_latest, removed_dev]
    
    return [
        source_headings,
        list(map(lambda x: x if len(str(x)) else "--", result))
    ]



def process_sinks(stable_dataflows, dev_dataflows, repo_name,key='storages'):

    headings = [ 
        'repo_name',
        f'Number of {key} sinks (base)',
        f'Number of {key} sinks (latest)',
        f'List of {key} Sinks (base)',
        f'List of {key} Sinks ( Latest )',
        '% of change w.r.t base',
        f'New {key} Sinks added in Latest',
        f'Existing {key} Sinks remvoed from Latest'
    ]
    storages_stable = stable_dataflows[key]
    storages_dev = dev_dataflows[key]

    stable_sinks = len(storages_stable) if (len(storages_stable)) else 0
    dev_sinks = len(storages_dev) if (len(storages_dev)) else 0


    sink_names_stable = set()
    sink_names_dev = set()
    for storage in storages_stable:
        for sink in storage['sinks']:
            sink_names_stable.add(sink['name'])
            
    for storage in storages_dev:
        for sink in storage['sinks']:
            sink_names_dev.add(sink['name'])

    sink_names_stable = '\n'.join(sink_names_stable)    
    sink_names_dev = '\n'.join(sink_names_dev)    



    # percent change in latest sources wrt stable release
    try:
        percent_change = f'{round((((dev_sinks - stable_sinks) / stable_sinks) * 100),2)}%'   
    except:
        percent_change = '0.00%'
    new_latest = '\n'.join(set(sink_names_dev.split('\n')) - set(sink_names_stable.split('\n')))
    removed_dev = '\n'.join(list(set(sink_names_stable.split('\n')) - set(sink_names_dev.split('\n'))))

    result = [repo_name, stable_sinks, dev_sinks, sink_names_stable, sink_names_dev, percent_change, new_latest, removed_dev]

    return [headings, list(map(lambda x: x if len(str(x)) else "--", result))]



def process_leakages(stable_dataflows, dev_dataflows, repo_name,key='leakages'):
    headings = [ 
        'repo_name',
        f'Number of {key} sinks (base)',
        f'Number of {key} sinks (latest)',
        f'List of {key} Sinks (base)',
        f'List of {key} Sinks ( Latest )',
        '% of change w.r.t base',
        f'New {key} Sinks added in Latest',
        f'Existing {key} Sinks remvoed from Latest'
    ]

    stable_leakages = stable_dataflows[key]
    dev_leakages = dev_dataflows[key]

    num_stable_leakages = len(stable_leakages)
    num_dev_leakages = len(dev_leakages)


    leakage_names_stable = '\n'.join(list(map(lambda x: x['sourceId'], stable_leakages)))
    leakage_names_dev = '\n'.join(list(map(lambda x: x['sourceId'], dev_leakages)))

    try:
        percent_change = f'{round((((num_dev_leakages - num_stable_leakages) / num_stable_leakages) * 100),2)}%'   
    except:
        percent_change = '0.00%'
    new_latest = '\n'.join(set(leakage_names_dev.split('\n')) - set(leakage_names_stable.split('\n'))) 
    removed_dev = '\n'.join(list(set(leakage_names_stable.split('\n')) - set(leakage_names_dev.split('\n'))))
    
    result = [repo_name, num_stable_leakages, num_dev_leakages, leakage_names_stable, leakage_names_dev, percent_change, new_latest, removed_dev]
    
    return [
        headings,
        list(map(lambda x: x if len(str(x)) else "--", result))
    ]

if __name__ == "__main__":
    main()