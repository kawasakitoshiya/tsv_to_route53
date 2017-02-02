import sys
import json
import datetime


def main(tsv_path):
    with open(tsv_path) as f:
        lines = map(lambda x: x.strip().split('\t'), f.readlines())

    changes = []
    for l in lines:
        v = l[3]
        v = '"{}"'.format(v)
        record = {
            "Action": "CREATE",
            "ResourceRecordSet": {
                "Name": l[0],
                "Type": l[1],
                "TTL": int(l[2]),
                "ResourceRecords": [
                    {
                        "Value": v
                    }
                ]
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
