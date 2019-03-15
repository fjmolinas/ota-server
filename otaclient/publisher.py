import argparse
import json
import requests


def parse_args():
    parser = argparse.ArgumentParser(description="OTA publisher")
    parser.add_argument('--ota-host', type=str, default="localhost",
                        help="OTA server host.")
    parser.add_argument('--ota-port', type=int, default=8080,
                        help="OTA server port.")
    parser.add_argument('manifest', type=str, help="manifest file")
    parser.add_argument('slot0', type=str, help="slot0 binary file")
    parser.add_argument('slot1', type=str, help="slot1 binary file")
    parser.add_argument('publish_id', type=str,
                        help="published version identifier, should be unique")
    parser.add_argument('node_url', type=str,
                        help="url to use to notify the device of an update")
    return parser.parse_args()


def main(args):
    response = requests.post(
        'http://{}:{}/publish'.format(args.ota_host, args.ota_port),
        files=dict(manifest=open(args.manifest, 'rb').read(),
                   slot0=open(args.slot0, 'rb').read(),
                   slot1=open(args.slot1, 'rb').read()),
        data=dict(publish_id=args.publish_id, node_url=args.node_url))
    print('{}: {}'.format(response.status_code, response.reason))


if __name__ == '__main__':
    try:
        main(parse_args())
    except Exception as exc:
        print("Error: {}".format(exc))
