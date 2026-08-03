\# Installation Guide



\## 1. Server Preparation



This section describes the required server environment and initial setup for deploying the automated incident response platform.



\### 1.1 Server Requirements



Recommended server configuration:



| Component        | Specification    |

| ---------------- | ---------------- |

| Operating System | Ubuntu 24.04 LTS |

| CPU              | 8 Cores          |

| RAM              | 16 GB            |

| Storage          | 100 GB           |



\---



\## 2. Install Docker and Docker Compose



Update the system packages and install required dependencies:



```bash

sudo apt update

sudo apt install git curl -y

```



Install Docker:



```bash

curl -fsSL https://get.docker.com | sudo bash

```



Install Docker Compose plugin:



```bash

sudo apt install docker-compose-plugin -y

```



Verify the installation:



```bash

docker --version

docker compose --version

```



\---



\# 3. Shuffle Installation



Shuffle is used as the SOAR platform to orchestrate incident response workflows.



\## 3.1 Clone Shuffle Repository



Clone the official Shuffle repository:



```bash

git clone https://github.com/Shuffle/Shuffle

```



Navigate to the Shuffle directory:



```bash

cd Shuffle/

```



\---



\## 3.2 Create Database Directory



Create the database directory used for persistent storage:



```bash

mkdir shuffle-database

```



Set the correct ownership:



```bash

sudo chown -R 1000:1000 shuffle-database

```



This directory stores:



\* Shuffle database files

\* PostgreSQL data

\* Persistent container volumes



\---



\## 3.3 Start Shuffle Services



Deploy Shuffle using Docker Compose:



```bash

sudo docker compose up -d

```



Check running containers:



```bash

sudo docker ps

```



Verify the web interface:



```bash

curl http://<SERVER-IP>:3001

```



\---



\## 3.4 Access Shuffle Web Interface



Open the browser:



```

http://<SERVER-IP>:3001

```



Complete the initial setup from the Shuffle web interface.



\---



\# 4. Shuffle Swarm Configuration



Edit the Shuffle Docker Compose configuration:



```bash

nano \~/Shuffle/docker-compose.yml

```



Disable the Swarm configuration:



```yaml

\# SHUFFLE\_SWARM\_CONFIG=run

```



Restart Shuffle services:



```bash

sudo docker compose down

sudo docker compose up -d

```



\## Troubleshooting Note



Incorrect Swarm configuration may cause:



\* Worker nodes failing to join the cluster

\* Webhook events received but workflows not executed

\* API requests hanging

\* Integration failures with:



&#x20; \* FortiGate API

&#x20; \* AbuseIPDB API

&#x20; \* Telegram Bot API



\---



\# 5. Configure Shuffle Webhook



The webhook is used to receive security alerts from Wazuh.



Create a webhook:



```

Workflows → Webhooks → Create Webhook

```



The generated webhook URL will have the following format:



```bash

https://<SERVER-IP>:3001/api/v1/hooks/<HOOK\_ID>

```



Save this URL for Wazuh integration.



\---



\# 6. Integrate Wazuh with Shuffle



This configuration is performed on the Wazuh Manager server.



\## 6.1 Edit Wazuh Configuration



Open the configuration file:



```bash

sudo nano /var/ossec/etc/ossec.conf

```



Add the Shuffle integration:



```xml

<integration>

&#x20; <name>shuffle</name>

&#x20; <hook\_url><SHUFFLE\_WEBHOOK\_URL></hook\_url>

&#x20; <level><MINIMUM\_ALERT\_LEVEL></level>

&#x20; <rule\_id><TRIGGER\_RULE\_IDS></rule\_id>

&#x20; <alert\_format>json</alert\_format>

</integration>

```



Configuration parameters:



| Parameter    | Description                       |

| ------------ | --------------------------------- |

| hook\_url     | Shuffle webhook endpoint          |

| level        | Minimum alert severity            |

| rule\_id      | Wazuh rules triggering automation |

| alert\_format | Alert format sent to Shuffle      |



\---



\## 6.2 Restart Wazuh Manager



Apply the configuration:



```bash

sudo systemctl restart wazuh-manager

```



Verify service status:



```bash

sudo systemctl status wazuh-manager

```



\---



\# 7. Workflow Deployment



The Shuffle workflow contains the following automation stages:



```

Wazuh Alert

&#x20;     |

&#x20;     v

Webhook Trigger

&#x20;     |

&#x20;     v

Alert Data Parsing

&#x20;     |

&#x20;     v

AbuseIPDB Reputation Check

&#x20;     |

&#x20;     v

Risk Evaluation

&#x20;     |

&#x20;     v

FortiGate IP Blocking

&#x20;     |

&#x20;     v

Telegram Notification

```



\---



\# 8. Next Steps



After completing the installation:



1\. Configure Shuffle applications:



&#x20;  \* HTTP Client

&#x20;  \* FortiGate API

&#x20;  \* Telegram Bot



2\. Import the incident response workflow.



3\. Test the automation flow:



```

Wazuh Alert

→ Shuffle

→ Threat Intelligence Check

→ FortiGate Block

→ Telegram Notification

```



The environment is now ready for automated incident response.



