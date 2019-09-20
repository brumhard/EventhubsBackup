# Prometheus

NOT FITTING FOR THE MONITORING SETUP

[Link to picture if the preferred architecture](https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwisnuyrrd_kAhXFy6QKHb7XCxoQjRx6BAgBEAQ&url=https%3A%2F%2Fgithub.com%2Fprometheus%2Fprometheus&psig=AOvVaw1AvYJFXEcHXIUILurHFFgL&ust=1569067299455208)

Histogramm or Summary  
https://prometheus.io/docs/practices/histograms/  
histogram or summary? (probably histogram as python doesn't implement quantiles yet)

[Jobs and instances \| Prometheus](https://prometheus.io/docs/concepts/jobs_instances/)
1 job for all api endpoints of sso?
automatic up metric for all scraped hosts

[When to use the Pushgateway \| Prometheus](https://prometheus.io/docs/practices/pushing/)
The Pushgateway seems to be the only way implement the targeted infrastructure with a service bus but the usage is not recommended.
-> where should the client be placed?

for online services there should be client side and server side monitoring ([Instrumentation \| Prometheus](https://prometheus.io/docs/practices/instrumentation/#online-serving-systems))

- -> server side in the API code

- -> on an extry client that checks failed requests request time...
  - -> no service bus as the client code needs to be implemented where the request is executed

[Instrumentation \| Prometheus](https://prometheus.io/docs/practices/instrumentation/#online-serving-systems)
Server side implementation?

[Configuration \| Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config)
For Kubernetes Service discovery?

## infrastructure questions

- service foreach host to be monitored?
- 1 service for all hosts? wheres the limit for service
- file based service discovery? or kubernetes ?
- prometheus and monitoring services in one cluster?

-> not applicable to backup architecture
