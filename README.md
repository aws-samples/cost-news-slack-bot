# rss_to_slack_webhook

Python tool to read an RSS feed and selectively publish articles, based on keywords, to Slack via Webhook

This tool checks the AWS 'What's New' RSS feed every minute for announcements related to cost optimization. 

Code adapted from: https://timothybramlett.com/recieving_notifications_of_rss_feeds_matching_keywords_with_Python.html

Key word filter can be updated for your needs. 

Run this script with a cronjob every minute by adding the following to your crontab:

```
* * * * * /usr/bin/python3 /home/ec2-user/rss_webhook/rss_webhook.py
```


## Deployment with Slack


Walkthrough 

We will walkthrough four steps to create the solution:

1. Create a new slack channel for AWS Announcements - This will be where the AWS announcements will be published
2. Deploy AWS CloudFormation Stack - Contains infrastructure which will scan for updates and feed them into the channel
3. Test deployment - The first run of the code will ensure all settings have been configured correctly so you can see the output in the channel
4. Start sharing - Guidance on how to use this channel to get the most out of it

Prerequisites

For this walkthrough, you should have the following prerequisites: 

* An AWS account
* IAM permissions in the account to deploy a Amazon CloudFormation template with a AWS lambda function, AWS IAM Role and Amazon S3 Bucket
* A Slack Workspace to create the channel in (Instructions to create slack app if you don’t have one)
* The ability to Activate Incoming Webhooks or request this in your Organization 

### 1 Create Slack Channel

For this solution we will create a slack channel for the cost announcements. For this we have linked to the official Slack guidance

1. Open your Slack Workspace and Click Add Channels

2. Name your channel #aws-cost-optimization-news-and-announcements. Once created, click on the drop down 
![1.2.NameChannel.png](/screen-shots/1.2.NameChannel.png)

3. Click the Integrations tab and click Add a Workflow
![1.3.Intergrations.png](/screen-shots/1.3.Intergrations.png)

4. Click Create. In the pop up call your workflow aws-cost-optimization-workflow

5. Click Select next to Webhook
![1.5.SelectWebhook.png](/screen-shots/1.5.SelectWebhook.png)
6. Click Add Variable 
![1.6.AddVariable.png](/screen-shots/1.6.AddVariable.png)

7. In the pop up add ‘title’ and leave as text. Click Done. 
![1.7.Add_Title_To_Pop_Up.png](/screen-shots/1.7.Add_Title_To_Pop_Up.png)

8. Repeat for ‘description’ and ‘url’. When done click Next
![1.8.Repeat_step_beforew_for Description_Title.png](/screen-shots/1.8.Repeat_step_beforew_for Description_Title.png)

9. Click Add Step 

10. Select Send a message from the list

11. Find your channel you made earlier in the drop down box. Then in the text box insert your variables, each one on a new line. Highlight the title and change it to bold. Click Save
![1.11.Send_Message_to_channel.png](/screen-shots/1.11.Send_Message_to_channel.png)

12. Click the Publish button

13. Copy your Webhook as we will use this in the next step. Close this pop out. 

![1.13.Copy_Workflow_link.png](/screen-shots/1.13.Copy_Workflow_link.png)

14. You should have a Webhook that looks like below. Keep a copy of this to hand as we will use in the next section:

![1.14.Webhook.png](/screen-shots/1.14.Webhook.png)


### 2 Deploy AWS CloudFormation Stack

Architecture 

![2.Architecture_digaram.png](/screen-shots/2.Architecture_digaram.png)
Figure 3: AWS CloudFormation Architecture Diagram


In this section we will deploy the resources for this solution in your AWS account

1. Log in to your AWS account
2. Link to CloudFormation stack you have cloned from this repo

3. Update the Webhook parameter with your web hook from section 1. Tick the acknowledge box and click Create stack. You can see the repo here. 

4. Wait until the stack has finished deploying and is showing as CREATE-COMPLETE (estimated 3 minuets)

### 3 Test Deployment

In this section we will test your deployment. 


1. In your CloudFormation stack, click Resources and look for your lambda function CFM_RSS_Lambda. Click the blue hyperlink


1. This link takes you to the lambda console. Scroll down and click on the Test tab and then click the orange Test button on the right 


1. You should see a green box appear showing a successful execution

![3.4.Successful_Slack_message.png](/screen-shots/3.4.Successful_Slack_message.png)

1. In your cost optimization slack channel, you should now see


### 4 Start Sharing 

Below are some tips to ensure people access and use the announcements you share

* Allow channel to be open to anyone 
* Advertise to your teams from different app teams/FinOps
* Choose your highlights and share in week updates
* Use Slack emoji feature to get devs to react to posts they found interesting or will implement. this way you can track engagement. 



### Cleaning up 

To avoid incurring future charges, delete the news bot.

1. Go your AWS CloudFormation Console and find the RSS Stack
2. Click on Resources and find your S3Bucket name and copy the physical ID



1. Go to your S3 Console and Search for the physical ID and click Empty. Once complete go back and click the Delete button


1. Go to your CloudFormation Console. Click on your Stack Delete CloudFormation stack and click Delete






Lambda Layer:

https://towardsdatascience.com/python-packages-in-aws-lambda-made-easy-8fbc78520e30

mkdir folder
cd folder
virtualenv v-env
source ./v-env/bin/activate
pip install BeautifulSoup4
pip install feedparser
pip install requests
pip install urllib3==1.26.15 -t ./python --no-user --upgrade
deactivate

mkdir python
cd python
cp -r ../v-env/lib/python3.10/site-packages/* .
cd ..
zip -r panda_layer.zip python
aws lambda publish-layer-version --layer-name rss --zip-file fileb://rss.zip --compatible-runtimes python3.10
## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

