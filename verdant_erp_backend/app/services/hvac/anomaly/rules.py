def detect_temperature_anomaly(records):

    temps = [r.temperature for r in records if r.temperature is not None]

    if len(temps) < 5:
        return []

    avg = sum(temps) / len(temps)

    if avg > 90:

        return [{
            "type": "overheat",
            "severity": "high",
            "title": "High temperature detected",
            "description": f"Average temperature is {avg:.2f}°",
            "snapshot": {
                "avg_temp": avg,
                "samples": len(temps)
            }
        }]

    return []


def detect_energy_spike(records):

    anomalies = []

    for i in range(1, len(records)):

        if records[i].energy_kw and records[i-1].energy_kw:

            delta = records[i].energy_kw - records[i-1].energy_kw

            if delta > 10:

                anomalies.append({
                    "type": "energy_spike",
                    "severity": "medium",
                    "title": "Energy consumption spike",
                    "description": f"Spike detected: {delta:.2f} kW",
                    "snapshot": {
                        "delta": delta
                    }
                })

    return anomalies


def detect_pressure_instability(records):

    pressures = [r.pressure for r in records if r.pressure is not None]

    if len(pressures) < 5:
        return []

    if (max(pressures) - min(pressures)) > 15:

        return [{
            "type": "pressure_instability",
            "severity": "medium",
            "title": "Pressure instability detected",
            "description": "High variation in system pressure",
            "snapshot": {
                "max": max(pressures),
                "min": min(pressures)
            }
        }]

    return []