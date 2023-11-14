# Your Actie project

aggregator is a publish/subscribe tools that manages aggregated notifications for users

there are two actors: user and topic

users can subscribe to topics and select the aggregation policy

topics maintains a list of messages and inform user subscribers when new messages are added

when a user receive a new message from a topic, it wait creating the notification till the aggregation policy for the topic is triggered

if someone subscribe to a new topic, the topic send to the aggregator the list of previously published messages


topics: tempo oggi, news daily


feed - content aggregator

customized-per-user


custom content aggregator feed


focusfeed is a customizable content aggregator feed

it allows users to subscribe to topics and set custom aggregation policies

## actor implementation:

user:
- maintains a list of subscribed topics and an aggregation policy for each
- deliver aggregated feeds depending on the chosen policy

topic:
- maintains a list of published contents
- notifies subscribers when new contents are added
- allow subscribe/unsubscribe
- send to new subscribers all previous contents

## functional implementation

subscribe(topic, user):
- add subscriber to topic
- call aggregate

unsubscribe(topic, user):
- remove subscriber to topic

set_policy(topic, user, policy):
- update aggregation policy of the subscription

publish(topic, content):
- add a content to a topic
- call aggregate for each subscriber

notify(topic, user):
- deliver aggregated feed for users depending on the chosen policies
- if no aggregation was sent before, send 

this implementation needs a db to store contents, subscriptions and aggregation policies

content: topic, timestamp, body

subscription: topic, user, aggregation_policy, timestamp

