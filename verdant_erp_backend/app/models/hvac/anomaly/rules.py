def detect_temperature_anomaly(data):

    if len(data) < 5:
        return []

    temps = [d.temperature for d in data if d.temperature is not None]

    avg = sum(temps) / len(temps)

    anomalies = []

    if avg > 90:

        anomalies.append({
            "type": "overheat",
            "severity": "high",
            "title": "High temperature detected",
            "description": f"Average temp {avg:.2f} exceeds safe threshold",
            "snapshot": {
                "avg_temp": avg,
                "samples": len(temps)
            }
        })

    return anomalies


def detect_energy_spike(data):

    anomalies = []

    for i in range(1, len(data)):

        if data[i].energy_kw and data[i-1].energy_kw:

            diff = data[i].energy_kw - data[i-1].energy_kw

            if diff > 10:

                anomalies.append({
                    "type": "energy_spike",
                    "severity": "medium",
                    "title": "Energy spike detected",
                    "description": f"Spike of {diff:.2f} kW detected",
                    "snapshot": {
                        "delta": diff
                    }
                })

    return anomalies


def detect_pressure_instability(data):

    pressures = [d.pressure for d in data if d.pressure]

    if len(pressures) < 5:
        return []

    max_p = max(pressures)
    min_p = min(pressures)

    if (max_p - min_p) > 15:

        return [{
            "type": "pressure_instability",
            "severity": "medium",
            "title": "Pressure instability",
            "description": "Pressure variation too high",
            "snapshot": {
                "max": max_p,
                "min": min_p
            }
        }]

    return []