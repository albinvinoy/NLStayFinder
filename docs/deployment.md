# Deploying NLStayFinder on AWS

This document provides instructions for deploying the NLStayFinder application on AWS.

## Prerequisites

- AWS account with appropriate permissions
- AWS CLI configured locally
- Docker installed locally

## Architecture Overview

The deployment architecture consists of:

- **EC2 Instance**: Hosts the main application
- **RDS PostgreSQL**: Database for storing apartment listings
- **Lambda Function**: Scheduled task for running scrapers
- **CloudWatch Events**: For scheduling Lambda executions
- **Elastic Load Balancer (Optional)**: For handling traffic and SSL termination

## Deployment Steps

### 1. Set up RDS PostgreSQL Database

1. Log in to the AWS Management Console
2. Navigate to RDS Service
3. Click "Create database"
4. Select "PostgreSQL"
5. Choose a suitable DB instance size (e.g., db.t3.micro for development)
6. Configure settings:
   - DB instance identifier: `nlstayfinder-db`
   - Master username: `postgres` (or your preferred username)
   - Set a secure password
7. Configure advanced settings:
   - Initial database name: `nlstayfinder`
   - Set VPC, subnet group, and security group as needed
8. Create the database
9. Note the endpoint URL for later use

### 2. Create EC2 Instance

1. Navigate to EC2 Service
2. Click "Launch instance"
3. Select an Amazon Linux 2 AMI
4. Choose an instance type (t2.micro for testing, larger for production)
5. Configure instance details:
   - Network: Same VPC as your RDS instance
   - IAM role: Create or select a role with permissions for RDS access
6. Add storage as needed (20GB is sufficient for most deployments)
7. Configure security group:
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) and HTTPS (port 443) from anywhere
   - Allow port 8000 from within the VPC
8. Launch the instance and select a key pair
9. Connect to the instance via SSH

### 3. Set Up EC2 Environment

```bash
# Update the system
sudo yum update -y

# Install Docker
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo yum install git -y

# Clone the repository
git clone https://github.com/yourusername/NLStayFinder.git
cd NLStayFinder
```

### 4. Configure Application

1. Create a `.env` file with production settings:

```bash
cat > .env << EOL
# PostgreSQL Database Configuration
POSTGRES_SERVER=<your-rds-endpoint>
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your-password>
POSTGRES_DB=nlstayfinder

# Scraper Configuration
SCRAPER_INTERVAL_HOURS=24

# AWS Configuration
AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
AWS_REGION=<your-region>
EOL
```

### 5. Deploy Application

```bash
# Build and start the application
docker-compose -f docker-compose.prod.yml up -d

# Initialize the database (if needed)
docker-compose -f docker-compose.prod.yml exec web python -m scripts.create_tables
```

### 6. Set Up Lambda for Scheduled Scraping

1. Navigate to Lambda in the AWS Console
2. Create a new function:
   - Name: `nlstayfinder-scraper`
   - Runtime: Python 3.9
   - Execution role: Create a new role with basic Lambda permissions
3. Configure the function:
   - Add RDS access permissions to the role
   - Set environment variables for database connection
4. Create a deployment package:

```bash
# On your local machine or EC2 instance
mkdir lambda_package
cd lambda_package

# Create the Lambda handler
cat > lambda_function.py << EOL
import os
import sys
import asyncio
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

# Import scraper code (you'll need to include your scraper files)
# This is a simplified example
def lambda_handler(event, context):
    # Set up database connection
    db_host = os.environ['DB_HOST']
    db_user = os.environ['DB_USER']
    db_pass = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']
    
    # Initialize scraper 
    # Your scraper initialization code here
    
    # Run scraper
    # Your scraper running code here
    
    return {
        'statusCode': 200,
        'body': 'Scraper completed successfully'
    }
EOL

# Create requirements.txt
cat > requirements.txt << EOL
sqlalchemy==2.0.20
asyncpg==0.28.0
beautifulsoup4==4.12.2
requests==2.31.0
EOL

# Install dependencies
pip install -r requirements.txt -t .

# Create deployment package
zip -r ../lambda_deployment_package.zip .
```

5. Upload the deployment package to Lambda
6. Set up a CloudWatch Event Rule to trigger the Lambda function on schedule

### 7. Set Up Nginx as Reverse Proxy (Optional)

```bash
# Install Nginx
sudo amazon-linux-extras install nginx1 -y
sudo systemctl start nginx
sudo systemctl enable nginx

# Configure Nginx as reverse proxy
sudo tee /etc/nginx/conf.d/nlstayfinder.conf << EOL
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOL

# Test configuration and restart Nginx
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Set Up SSL with Let's Encrypt (Optional)

```bash
# Install Certbot
sudo amazon-linux-extras install epel -y
sudo yum install certbot python-certbot-nginx -y

# Obtain and install certificate
sudo certbot --nginx -d your-domain.com
```

## Monitoring and Maintenance

### Monitoring

- Set up CloudWatch Alarms for EC2 and RDS metrics
- Configure logging to CloudWatch Logs
- Set up alerts for application errors

### Backup Strategy

- Configure automated RDS snapshots
- Implement a database backup retention policy
- Set up EC2 AMI backups as needed

### Scaling Considerations

- Use Auto Scaling Groups for the EC2 instances
- Consider using a load balancer for high availability
- Monitor database performance and scale as needed 