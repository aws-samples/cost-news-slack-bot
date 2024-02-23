# rss_to_slack_webhook

Python tool to read an RSS feed and selectively publish articles, based on keywords, to Slack via Webhook

This tool checks the AWS 'What's New' RSS feed every minute for announcements related to cost optimization.  

Code adapted from: https://timothybramlett.com/recieving_notifications_of_rss_feeds_matching_keywords_with_Python.html

Key word filter can be updated for your needs. This focuses on Cost based posts.

Run this script with a cronjob every minute by adding the following to your crontab:

```
* * * * * /usr/bin/python3 /home/ec2-user/rss_webhook/rss_webhook.py
```


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

