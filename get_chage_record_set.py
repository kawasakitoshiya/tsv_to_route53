import sys
import json
import datetime
from collections import defaultdict


def main(tsv_path):
    with open(tsv_path) as f:
        lines = map(lambda x: x.strip().split('\t'), f.readlines())
    dic = defaultdict(dict)
    for l in lines:
        name = l[0]
        type = l[1]
        v = l[3]
        if '=' in l[3]:
            v = '"{}"'.format(v)

        k = '{}-{}'.format(name, type)
        if 'values' not in dic[k]:
            dic[k]['values'] = []
        dic[k]['values'].append(v)
        dic[k]['ttl'] = int(l[2])
        dic[k]['name'] = name
        dic[k]['type'] = type
    changes = []
    for k, v in dic.items():
        record = {
            "Action": "CREATE",
            "ResourceRecordSet": {
                "Name": v['name'],
                "Type": v['type'],
                "TTL": v['ttl'],
                "ResourceRecords": [{"Value": e} for e in v['values']],
            }
        }
        changes.append(record)
    output = {
        "Changes": changes
    }
    output_filename = '{:%Y%m%d_%H%M%S}.json'.format(datetime.datetime.now())
    with open(output_filename, 'w') as f:
        f.write(json.dumps(output))

    print 'generated changeset file, execute command below.'
    print '$ aws route53 change-resource-record-sets --hosted-zone-id ${{R53_ZONE_ID}} --change-batch file://{}'.format(output_filename)
    print 'you can get R53_ZONE_ID by $aws route53 list-hosted-zones'

if __name__ == '__main__':
    tsv_path = sys.argv[1]
    main(tsv_path)
