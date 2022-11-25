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

    process_sources_data(report, previous_data['sources'], current_data['sources'])
    process_processing_data(report, previous_data['processing'], current_data['processing'])
    
    if (len(previous_data['collections'])):
        process_collection(report, previous_data['collections'][0]['collections'], current_data['collections'][0]['collections'])
    process_violations(report, previous_data['violations'], current_data['violations'])
    create_csv(report, filename)

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


if __name__ == "__main__":
    main()