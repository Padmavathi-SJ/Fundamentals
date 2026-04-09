from circuit_breaker import failures

cache_hits = {
    "user-service": 0,
    "order-service": 0,
    "product-service": 0
}

def increment_cache(service):
    cache_hits[service] += 1

def show_dashboard():
    print("\n=== Health Dashboard ===")
    print("+-------------+----------+----------+-----------+-------------------+")
    print("| Service     | Status   | Failures | Circuit   | Cache Hits        | ")
    print("+-------------+----------+----------+-----------+-------------------+")

    for service in ["user-service", "order-service", "product-service"]:
        fail = failures.get(service, 0)
        status = "DOWN" if fail >= 5 else "UP"
        circuit = "OPEN" if fail >= 5 else "CLOSED"

        print(f"| {service:<16} | {status:<6} | {fail:<8} | {circuit:<8} | {cache_hits[service]:<11} |")

