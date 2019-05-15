import json


def test_check_default_gateways(local_salt_client, nodes_in_group):
    netstat_info = local_salt_client.cmd(
        tgt="L@"+','.join(nodes_in_group),
        param='ip r | sed -n 1p',
        expr_form='compound')

    gateways = {}

    for node in netstat_info.keys():
        gateway = netstat_info[node]
        if isinstance(gateway, bool):
            gateway = 'Cannot access node(-s)'
        if gateway not in gateways:
            gateways[gateway] = [node]
        else:
            gateways[gateway].append(node)

    assert len(gateways.keys()) == 1, \
        "There were found few gateways: {gw}".format(
        gw=json.dumps(gateways, indent=4)
    )
