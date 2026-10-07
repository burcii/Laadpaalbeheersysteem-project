When a charger has been sending messages for a while, and then the software is started, alle queued messages are received. The software will then start handling them, starting from the oldest message. This usually results in sending lots of register replies, while only a single one is needed. This could be improved by removing all similar messages from the in-queue as soon as a new one is received. The inbound queue needs to be a bit more organized for that though.





Create open source implementation of the EVBox ChargePoint management.

Goal is to do whatever a CP can, but better, and open.

Fix all the robustness issues, with proper validation and state machines

Support more CBs. Maybe the limiting factor is the bus, not sales.

Support multiple busses

First milestone is to work stand-alone. Future milestones could include connecting to EVBox backend and/or alternatives.



The word ChargePoint is used for more things and companies.



