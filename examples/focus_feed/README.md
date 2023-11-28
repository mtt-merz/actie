# Focus Feed

Focus Feed is the real-world application we developed to evaluates our work. Although not overlay complex, it contains all the key elements necessary for a meaningful evaluation of the Actie framework.

Focus Feed represents an enhanced version of the classic publish-subscribe application, centered around two primary entities: users and topics. Its basic behavior is simple: users subscribe to topics of interest and receive notifications when new articles are published under these topics. The novelty comes at this point, increasing system complexity. When subscribing to a topic, users are asked to define a notification policy that dictates the aggregation of topic articles prior to delivery. As a result, users are notified not for each new article but when an article triggers the specified policy. Notification, therefore, consists of a collection of articles, delivered at user-defined intervals. For example, this mechanism can be seen as a news feed that sends subscribers the main events from the previous day each morning, or a group chat where members choose to receive periodic notifications, rather than for every message. The application’s name, Focus Feed, reflects its purpose: to help users stay focused by reducing the frequency of notifications for new topic content.

Now that we clarified the application behavior from a high-level perspective point of view, we present and formalize the desired functionalities that both implementations should offer. This is a set of requirements, that outlines the actions the system should support. These actions will later guide our evaluation process.

**Subscribe**: This action enables a user to begin following a topic. Upon starting a subscription, the user can provide a desired policy. If no policy is provided, a default one should be applied.

**Unsubscribe**: This action allows a user to stop following a topic. After this action, no further articles related to that topic should be sent to the user.

**Publish**: Through this action, new articles are added to a topic. All subscribers of the topic should be informed of the new publication, thus enabling the application of the specified policies and, if necessary, the delivery of aggregated content.
Aggregate: This action is triggered for each topic subscriber whenever new articles are added. It checks whether the specified policies are matched, determining if subscribers should be notified.

**Set policy**: This action permits a user to modify an existing policy for a topic.

But what do we mean by “policy”? From a conceptual point of view, with this term we refer to any rule that can lead to content aggregation. In this context, we have simplified the notion since it is not the central focus of this implementation. Thus, the only policy that users can specify regards the number of messages in each notification. In this way, the system should notify the user as soon as the specified threshold for a particular topic is reached. Note that the policy mechanism can be conveniently expanded with minor adjustments.
