import csv 
import json

def main():

    previous_file = open('value1.json')
    current_file = open('value2.json')

    previous_data = json.load(previous_file)
    current_data = json.load(current_file)

    report = []

    process_sources_data(report, previous_data['sources'], current_data['sources'])
    process_processing_data(report, previous_data['processing'], current_data['processing'])
    create_csv(report)

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

def create_csv(data):

    with open('Report.csv', "w") as value:
        report = csv.writer(value)
        for i in data:
            report.writerow(i)

if __name__ == "__main__":
    main()