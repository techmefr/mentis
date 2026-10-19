# § 3 — RabbitMQ

> Section 3 of `skills/messaging-conventions`. Read it when the broker is RabbitMQ. Reliability is shared three
> ways here: the queue type on the broker, confirms on the publisher, acknowledgements on the consumer. A weak
> link in any one of the three defeats the other two.

1. **Use a replicated queue type for anything you cannot lose.** Quorum queues are the documented default choice
   when a replicated, highly available queue is needed; the mirroring of classic queues was removed in RabbitMQ
   4.0, so advice and configuration that rely on it describe a feature that no longer exists. Streams are the
   other replicated structure, suited to very long backlogs and large fan-outs. A quorum queue is not the right fit
   for temporary or exclusive queues, for the lowest possible latency, for very long backlogs or for workloads that
   do not use confirms and manual acknowledgements, since its safety depends on them.
2. **Declare queues durable and publish messages as persistent** for important data. A non-durable queue or a
   transient message does not survive a node restart, whatever else is configured. Exclusive queues are tied to
   a connection and are never replicated.
3. **Enable publisher confirms; do not assume a written frame arrived.** A client that has written a message to
   its socket cannot tell whether the broker received it. In confirm mode the broker acknowledges each message once
   it has taken responsibility: for a persistent message in a durable queue that means it is on disk, for a quorum
   queue that a quorum of replicas has accepted it. Keep a map of unconfirmed messages by sequence number and
   republish those that were not confirmed after a failure. Transactions are the only other guarantee in the
   protocol and are far slower, so use confirms. Confirms are per publish and say nothing about consumers.
4. **A republish may duplicate, so the consumer is idempotent** (§1.3); the broker may have confirmed a message
   whose confirmation never reached the publisher.
5. **Know whether your message was routed.** An exchange that matches no queue drops the message and, with
   confirms on, still confirms it. If a message must reach at least one queue, publish it as mandatory and handle the
   returned message, or publish directly to a declared queue. In a publish-subscribe design with no listeners,
   dropping is correct.
6. **Consume with manual acknowledgement and a bounded prefetch.** Automatic acknowledgement counts a message as
   delivered the moment it is sent, so a connection or channel closing loses what was in flight, and with no bound
   on outstanding deliveries a fast broker can overwhelm a slow consumer until it runs out of memory. Use manual
   acknowledgements, acknowledge after the work is done and recorded (§1.2), and set the per-channel prefetch to
   limit unacknowledged deliveries. A prefetch of one maximises fairness and minimises throughput; raise it by
   measurement, and remember that acknowledgements can be batched to save traffic.
7. **Redelivery is normal, and requeue loops are a trap.** After a connection loss or a nack with requeue, the
   message is delivered again with the redelivered flag set (a hint, not a certainty). If every consumer rejects a
   message and requeues it, the message goes straight back to the front and loops, burning CPU and network. Reject
   it for good, route it to a dead-letter destination, or requeue after a delay; track the delivery count and stop.
8. **Use the quorum queue's poison-message protection.** Quorum queues count failed deliveries (exposed in a
   delivery-count header) and can be given a delivery limit after which the message is dead-lettered or dropped,
   which is the built-in guard against a message that can never be processed.
9. **Dead-lettering is at most once by default.** A dead-lettered message from a quorum queue is transferred with
   at-most-once guarantees unless the at-least-once strategy is enabled, which requires rejecting publishes on
   overflow rather than dropping from the head and costs more memory and CPU. Turn it on only when the dead-lettered
   messages must not be lost, and read the failure cases the documentation lists.
10. **Use heartbeats and automatic connection recovery,** and handle the failure of a connection or channel as a
    normal event: reopen, redeclare what is needed, republish unconfirmed messages, resume consuming. Heartbeats
    detect dead connections much sooner than the operating system does and keep idle connections alive through
    middleboxes.
11. **Alarms stop publishers.** When the broker raises a memory or disk alarm it blocks publishing connections.
    Monitor the alarms, queue lengths and the age of the oldest message, set limits on queue length or message
    time-to-live with a known overflow behaviour, and follow the broker's production checklist before going live.
12. **Access is per virtual host and per user.** Give each application its own user with permissions only on the
    resources it uses, a virtual host per environment or tenant, and TLS between clients and broker. Do not use
    the default guest account beyond a local test.

**Sources:** the RabbitMQ documentation read from its published documentation repository on 2026-10-02
(documentation dual-licensed Apache-2.0 or MPL-2.0): the reliability guide, acknowledgements and confirms,
consumers and prefetch, quorum queues (poison-message handling, at-least-once dead-lettering, when not to use),
publishers, heartbeats, resource alarms, access control, production checklist. The web site itself sits behind a
challenge page for automated readers and was not read. Version-bound: classic-queue mirroring was removed in
4.0; the documentation read describes a release at or after 4.3, where the delivery limit counts failed
deliveries rather than acquisitions, so confirm the counter semantics on the deployed version. Default values of
limits and timeouts are left to that version's documentation and are not recited. Point 4 is a consequence we draw (§1.3), not a quotation.
