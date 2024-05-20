import argparse
import paramiko

def ssh_connect_with_key(host):
    """ Attempt to establish an SSH connection using a private key. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            host,
            username='root',  # Customize as necessary
            key_filename='/root/.ssh/id_rsa',  # Customize as necessary
            timeout=5,
            banner_timeout=10
        )
        return client
    except Exception as e:
        print(f"\n__________________________________________________________________________________________________________________________\n\nNo direct route to {host}: {str(e)}\n__________________________________________________________________________________________________________________________")
        return None

def execute_command_on_host(client, command):
    """ Execute a command on the connected SSH host client. """
    if client is None:
        return "Connection failed", True

    try:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        connected_output = output.strip() or error.strip()
        # Connection failure detections
        if ("Connection refused" in connected_output or
    "Permission denied" in connected_output or
    "No route to host" in connected_output or
    "Unable to connect to port 22 on" in connected_output or
    "Host is unreachable" in connected_output):
    # Handle the error conditions here
            return connected_output, True
        return connected_output, False
    except Exception as e:
        return str(e), True

def attempt_to_access_unreachable_host(via_host_clients, target_host, command):
    """ Try reaching the unreachable host using all accessible host clients. """
    connection_attempts = []
    for via_host, via_host_client in via_host_clients.items():
        command_to_run = f"ssh -o StrictHostKeyChecking=no {target_host} '{command}'"
        output, failed = execute_command_on_host(via_host_client, command_to_run)
        if not failed:
            return output, via_host
        connection_attempts.append(output)
    return "\n".join(connection_attempts), None

def main():
    parser = argparse.ArgumentParser(description="Execute a command over SSH on multiple hosts.")
    parser.add_argument("command", help="Command to execute.")
    parser.add_argument("hosts", nargs="+", help="List of IP addresses of the hosts.")
    args = parser.parse_args()

    reachable_hosts = {}
    unreachable_hosts = []

    for host in args.hosts:
        client = ssh_connect_with_key(host)
        if client:
            reachable_hosts[host] = client
        else:
            unreachable_hosts.append(host)

    for host, client in reachable_hosts.items():
        output, failed = execute_command_on_host(client, args.command)
        if failed:
            unreachable_hosts.append(host)
        else:
            print(f"\n----------------------------------------------------------------------------------------------\n____________________Output for host {host}:____________________\n\n{output}\n")

    for host in unreachable_hosts:
        output, via_host = attempt_to_access_unreachable_host(reachable_hosts, host, args.command)
        if via_host:
            print(f"\n----------------------------------------------------------------------------------------------\n____________________Output for host {host} (accessed via {via_host}):____________________\n\n{output}\n")
        else:
            print(f"================================================================================================\n__________________Unable to reach host {host} via any other listed hosts.__________________\n\nError details:\n{output}")

if __name__ == "__main__":
    main()