pipeline {
    agent any
    
    stages {
        stage('Check Router Pings') {
            steps {
                sh '''
                echo "=== Pinging Routers from Jenkins ==="
                routers="192.168.121.101 192.168.121.102 192.168.121.103 192.168.121.104"
                for ip in $routers; do
                    echo "Checking ping to $ip..."
                    ping -c 2 $ip || true
                done
                '''
            }
        }
        
        stage('Check Router SSH Ports') {
            steps {
                sh '''
                echo "=== Checking SSH Port 22 on Routers ==="
                python3 -c '
import socket
routers = ["192.168.121.101", "192.168.121.102", "192.168.121.103", "192.168.121.104"]
for ip in routers:
    try:
        s = socket.create_connection((ip, 22), timeout=2)
        print(f"Router {ip} SSH port 22 is REACHABLE")
        s.close()
    except Exception as e:
        print(f"Router {ip} NOT reachable: {e}")
'
                '''
            }
        }

        stage('Backup Configurations via Ansible') {
            steps {
                sh '''
                echo "=== Running Ansible Playbook for Configuration Backup ==="
                ansible-playbook -i hosts.yml playbooks/backup.yml
                '''
            }
        }
    }
}
