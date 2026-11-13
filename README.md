# Netlab Jenkins CI/CD Lab (`netlab-jenkins-ci`)

A production-ready Network DevOps (NetDevOps) lab combining **netlab**, **containerlab**, **Cisco IOL routers**, and a **Jenkins CI/CD container** with persistent storage.

---

## 🏛️ Topology Architecture

- **Routers**: 4x Cisco IOL (`R1`, `R2`, `R3`, `R4`) running OSPF.
- **CI/CD Orchestrator**: 1x Linux container (`jenkins`) running Jenkins LTS.
- **Persistence**: Jenkins configuration, plugins, and build history persist via a local host bind mount (`./jenkins_home:/var/jenkins_home`).

---

## 🚀 Quick Start

### Prerequisites
- Python 3 with `netlab` installed (`pipx install networklab`)
- Containerlab and Docker installed and running
- Create and set permissions for the local Jenkins data directory:
  ```bash
  mkdir -p jenkins_home && sudo chown -R 1000:1000 jenkins_home
  ```

### 1. Start the Lab
```bash
netlab up
```

### 2. Access Jenkins
- Open your browser at: `http://localhost:8080`
- Retrieve the initial administrator password:
  ```bash
  docker exec clab-campus-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
  ```

### 3. Install Automation Tools Inside Jenkins
Provision required system tools and NetDevOps libraries inside the Jenkins container as the root user:
```bash
docker exec -u 0 clab-campus-jenkins apt-get update && apt-get install -y python3 python3-pip iputils-ping
docker exec -u 0 clab-campus-jenkins pip3 install ansible netmiko --break-system-packages
```

---

## 🧪 Jenkins Pipeline Test

Create a new **Pipeline** job in Jenkins (e.g., `Network-Health-Check`) and use the following pipeline script to validate ICMP reachability and SSH port access across all lab routers:

```groovy
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
    }
}
```

---

## 📦 Persistence & Teardown

- To stop the lab without losing Jenkins data:
  ```bash
  netlab down
  ```
- To completely clean up containers and network artifacts:
  ```bash
  netlab down --cleanup
  ```
  *(Note: Jenkins plugins and jobs persist in the local `./jenkins_home` directory on the host)*
